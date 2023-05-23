""" @File   : views
    
    @Author : BabyMuu
    @Time   : 2023/2/10 12:06
"""
import datetime
import json
from collections import defaultdict

import pandas as pd
from django.http import HttpResponse, JsonResponse
from requests import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet, ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from sklearn.cluster import KMeans

from gra.utils.Apriori import Apriori
from . import serialize
from .models import *
from .serialize import *
from user.models import Questions, Scores

from gra.utils.page import MyPageNumberPagination

class SimpleView(ViewSet):
    @action(methods=['GET'], detail=False)
    def student_analysis(self, request, *args, **kwargs):
        """学生知识点得分情况分析"""
        exam_id, stu_id = request.query_params.get('exam_id'), request.query_params.get('stu_id')
        if not exam_id or not stu_id:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={'msg': '请输入考试号和学生ID'})
        exam = Exam.objects.filter(exam_id=exam_id, stu_id=stu_id).first()
        if not exam:
            err = self._gen_stu_ana(exam_id)
            if err:
                return err
            print("生成完毕")
        else:
            print("已经生成")
        instance = Exam.objects.filter(exam_id=exam_id, stu_id=stu_id).first()
        serializer = serialize.ExamSerializer(instance)
        know_points = []
        levels = []
        for kps in serializer.data['know_point_situation']:
            know_points.append(kps['know_point'])
            levels.append(kps['level'])
        return JsonResponse(data={
            'know_points': know_points,
            'levels'     : levels
        }, status=status.HTTP_200_OK)

    @staticmethod
    def _gen_stu_ana(exam_id):
        """
            生成考试数据分析数据
            有错误: 返回 response
            无错误: 返回 None
        """
        ques = Questions.objects.filter(exam_id=exam_id).all()
        if not ques:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, msg={'msg': '考试不存在'})
        stus = Scores.objects.filter(exam_id=exam_id)
        if not stus:
            JsonResponse(status=status.HTTP_400_BAD_REQUEST, msg={'msg': '没有学生参与本次考试'})
        # 获取当场考试每个知识点的总分
        know_point_score = defaultdict(int)
        for i in ques:
            know_point_score[i.kno_point] += i.score
        # 获取每个学生每个知识点的得分
        d_stus = {}
        for stu in stus:
            stu_get_score = defaultdict(int)
            scores = stu.score_situation.split(',')
            for i in range(len(scores)):
                kno_point = ques[i].kno_point
                stu_get_score[kno_point] += float(scores[i]) / know_point_score[kno_point]
                stu_get_score[kno_point] = round(stu_get_score[kno_point], 2)
            d_stus[stu.student_id] = stu_get_score
        data = pd.DataFrame(d_stus)
        # 对每个知识点得分情况聚类
        ks = [KMeans(n_clusters=4, random_state=0) for i in range(len(data))]
        for i in range(len(data)):
            ks[i].fit(data.iloc[i].values.reshape(-1, 1))
        # 对得分情况进行分级
        for i in range(len(ks)):
            k = ks[i]
            kc = k.cluster_centers_
            y = k.labels_
            kc_list = sorted([i for i in kc[:, 0]])

            def my(x):
                if x == kc_list[0]:
                    return "差"
                elif x == kc_list[1]:
                    return "中"
                elif x == kc_list[2]:
                    return "良"
                else:
                    return "优"

            data.iloc[i] = [my(x) for x in kc[y]]

        dic_lst = []
        for key, value in data.to_dict().items():
            vl = []
            for k, v in value.items():
                vl.append(
                    {
                        'know_point': k,
                        'level'     : v,
                    }
                )
            dic_lst.append({
                'exam_id'             : exam_id,
                'stu_id'              : key,
                'know_point_situation': vl
            })
        for i in dic_lst:
            print(i)
        serializer = ExamSerializer(data=dic_lst, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    @action(methods=['GET'], detail=False)
    def exam_analysis(self, request, *args, **kwargs):
        exam_id = request.query_params.get('exam_id')
        apri_exam = ApriExam.objects.filter(exam_id=exam_id).first()
        if not apri_exam:
            rules = self._gen_exam_ana(exam_id)
        else:
            rules = apri_exam.apri_res
        rules = json.loads(rules)
        return JsonResponse(data={
            'rules': rules
        }, status=status.HTTP_200_OK)

    @staticmethod
    def _gen_exam_ana(exam_id):
        rule_order = Scores.objects.filter(exam_id=exam_id)
        dataset = []
        for i in rule_order:
            dataset.append(i.score_know_situation.split(','))
        print(dataset)
        a = Apriori(dataset)
        L, support_ = a.apriori(0.50)
        e = 0
        rules = a.gen_rate_rules(L, support_)

        def process(rule):
            rule = list(rule)
            rule[:2] = list(map(list, rule[:2]))
            rule[0] = "-".join(rule[0])
            rule[1] = "-".join(rule[1])
            rule[2] = round(rule[2], 2)
            return rule
        rules = list(map(process, rules))
        # rules = [
        #          ['有理数', '三角函数', 0.73],
        #          ['实数', '三角函数', 0.73],
        #          ['三角形', '三角函数', 0.9],
        #          ['实数', '有理数', 0.85],
        #          ['三角函数-实数', '四边形', 0.85],
        #          ['四边形-实数', '三角函数', 0.73],
        #          ['一次函数', '二次函数', 0.88],
        #          ['一次函数', '反比例函数', 0.75],
        #          ['二次函数', '反比例函数', 0.78],
        #          ['分式-整式', '因数分解', 0.73],
        #          ['圆-四边形', '几何', 0.88],
        #          ['一元一次方程', '一元二次方程', 0.88],
        #          ['一元一次方程', '二元二次方程', 0.89],
        #          ['二元一次方程', '一元二次方程', 0.93],
        #          ]
        rules = json.dumps(rules, ensure_ascii=False)
        serializer = ExamSerializer(data={
            'exam_id' : exam_id,
            'apri_res': rules
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return rules

class ExamsView(GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = my_model.Exams.objects.all()
    serializer_class = ExamsSerializer
    pagination_class = MyPageNumberPagination

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        new_data = self._gen_data(instance.id)
        serializer = self.get_serializer(instance, data=new_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return JsonResponse(data=serializer.data, status=status.HTTP_200_OK)

    def _gen_data(self, exam_id):
        s = Scores.objects.filter(exam_id=exam_id).values_list('score')
        s = pd.DataFrame(s)
        return {
            'avg_score': s.mean(),
            'max_score': s.max(),
            'min_score': s.min(),
        }
