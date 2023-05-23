""" @File   : serialize
    
    @Author : BabyMuu
    @Time   : 2023/2/10 12:06
"""
from rest_framework_mongoengine import serializers as s1
from rest_framework import serializers
from . import models as my_model

class ExamSerializer(s1.DocumentSerializer):
    class Meta:
        model = my_model.Exam
        fields = [
            'exam_id',
            'stu_id',
            'know_point_situation'
        ]

class ApriExamSerializer(s1.DocumentSerializer):
    class Meta:
        model = my_model.ApriExam
        fields = [
            'exam_id',
            'apri_res'
        ]

class ExamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = my_model.Exams
        fields = '__all__'
