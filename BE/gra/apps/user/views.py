from collections import defaultdict

import pandas as pd
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ViewSet
from django.db import transaction
from sklearn.cluster import KMeans

from . import serialize
from .filter import StudentFilter
from .models import *
from gra.utils.page import MyPageNumberPagination

# Create your views here.


class SimpleView(ViewSet):
    @action(methods=['POST'], detail=False)
    def login(self, request, *args, **kwargs):
        """登录"""
        ser = serialize.AccountSerializer(data=request.data,
                                          context={'request': request})
        if ser.is_valid(raise_exception=True):
            return JsonResponse({
                'username': ser.context['user'].username,
                'type'    : Users.UserTypes_choices[ser.context['user'].types],
                'name'    : ser.context['name'],
            })
        else:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, msg=ser.errors)

class UserView(GenericViewSet, CreateModelMixin):
    queryset = Users.objects.all()
    serializer_class = serialize.UserSerializer

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        if user.types == Users.UserTypes.STUDENT:
            instance = Students.objects.get(user_id=user.id)
            serializer = serialize.StudentSerializer(instance)
        else:
            instance = Teachers.objects.get(user_id=user.id)
            serializer = serialize.TeacherSerializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            data = request.data
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            types = serializer.data['types']
            if types in (Users.UserTypes.TEACHER, Users.UserTypes.ADMIN):
                serializer_ = serialize.TeacherSerializer
            else:
                serializer_ = serialize.StudentSerializer
            serializer_ = serializer_(data={
                'user_id' : serializer.context['id'],
                'name'    : serializer.context['name'],
                'class_id': serializer.context['classes']
            })
            serializer_.is_valid(raise_exception=True)
            serializer_.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class StudentView(ModelViewSet):
    queryset = Students.objects.all()
    serializer_class = serialize.StudentSerializer
    pagination_class = MyPageNumberPagination
    filterset_fields = ('name', 'class_id')

class TeacherView(ModelViewSet):
    queryset = Teachers.objects.all()
    serializer_class = serialize.TeacherSerializer
    pagination_class = MyPageNumberPagination

class ScoreView(ModelViewSet):
    queryset = Scores.objects.all()
    serializer_class = serialize.ScoreSerializer
    pagination_class = MyPageNumberPagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        ps = request.query_params
        stu_name, student_id = ps.get('stu_name'), ps.get('student_id')
        if stu_name:
            student = Students.objects.filter(name=stu_name).first()
            if not student:
                return JsonResponse(data={'msg': '学生不存在'}, status=status.HTTP_400_BAD_REQUEST)
            queryset = queryset.filter(student_id=student.user_id)
        elif student_id:
            queryset = queryset.filter(student_id=student_id)
        if not queryset:
            return JsonResponse(data={'msg': '学生不存在'}, status=status.HTTP_400_BAD_REQUEST)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class QuestionView(ModelViewSet):
    queryset = Questions.objects.all()
    serializer_class = serialize.QuestionSerializer
    pagination_class = MyPageNumberPagination
