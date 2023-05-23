""" @File   : urls
    
    @Author : BabyMuu
    @Time   : 2023/2/10 12:06
"""
from django.urls import re_path, path, include
from analysis import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('', views.SimpleView, 'simple')
router.register('exam', views.ExamsView, 'exam')
urlpatterns = [
    # path("create/", views.create, name="create"),
    path('', include(router.urls)),
]
