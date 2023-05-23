# from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser

class Questions(models.Model):
    class QueTypes:
        CHOICE = 1
        JUDGE = 2
        COMPLETION = 3
        SUBJECTIVE = 4

    QueTypes_choices = [(QueTypes.CHOICE, '选择题'), (QueTypes.JUDGE, "判断题"), (QueTypes.COMPLETION, "填空题"),
                        (QueTypes.SUBJECTIVE, '主观题')]
    kno_point = models.CharField(verbose_name='知识点', max_length=100)
    exam_id = models.IntegerField(verbose_name="考试ID")
    score = models.FloatField(verbose_name='题目分数')
    que_type = models.IntegerField(choices=QueTypes_choices, verbose_name="题型")
    que_num = models.IntegerField(verbose_name="题号")

class Scores(models.Model):
    score = models.FloatField("得分")
    student_id = models.IntegerField("学生ID")
    exam_id = models.IntegerField(verbose_name="考试ID")
    score_situation = models.CharField(max_length=200, verbose_name="得分情况")
    score_know_situation = models.CharField(max_length=200, verbose_name="知识点得分情况")

    @property
    def stu_name(self):
        return Students.objects.get(user_id=self.student_id).name

class Users(AbstractUser):
    class UserTypes:
        ADMIN = 0
        STUDENT = 1
        TEACHER = 2

    UserTypes_choices = [(UserTypes.ADMIN, '管理员'), (UserTypes.STUDENT, '学生'), (UserTypes.TEACHER, '教师')]
    telephone = models.CharField(max_length=11, default="10000000000")
    email = models.EmailField('邮箱地址', blank=True)
    icon = models.ImageField(upload_to='icon', default='icon/default.png')
    types = models.IntegerField(choices=UserTypes_choices, verbose_name="账号类型")

    def __str__(self):
        return self.username

class Teachers(models.Model):
    user_id = models.IntegerField()
    name = models.CharField(max_length=20)
    class_id = models.CharField(max_length=100, verbose_name="所教班级")

class Students(models.Model):
    user_id = models.IntegerField()
    name = models.CharField(max_length=20)
    class_id = models.IntegerField(verbose_name="所在班级")
