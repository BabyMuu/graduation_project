""" @File   : urls
    
    @Author : BabyMuu
    @Time   : 2023/2/9 14:11
"""
from django.urls import re_path, path, include
from user import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('', views.SimpleView, 'simple')
router.register('users', views.UserView, 'user')
router.register('questions', views.QuestionView, 'question')
router.register('scores', views.ScoreView, 'score')
router.register('stu', views.StudentView, 'student')
urlpatterns = [
    # path("create/", views.create, name="create"),
    path('', include(router.urls)),
]
