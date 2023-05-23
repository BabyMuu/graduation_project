""" @File   : filter
    
    @Author : BabyMuu
    @Time   : 2023/2/19 10:41
"""
from django_filters import rest_framework as filters
from . import models

class StudentFilter(filters.FilterSet):
    class Meta:
        model = models.Students
        fields = ['name', 'class_id']
