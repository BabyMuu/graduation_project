# from django.db import models

# Create your models here.
import mongoengine
from django.db import models

class KnowPointItem(mongoengine.EmbeddedDocument):
    know_point = mongoengine.StringField()
    level = mongoengine.StringField()

class Exam(mongoengine.Document):
    exam_id = mongoengine.IntField()
    stu_id = mongoengine.IntField()
    know_point_situation = mongoengine.ListField(mongoengine.EmbeddedDocumentField(KnowPointItem))

class Exams(models.Model):
    avg_score = models.FloatField(default=0)
    max_score = models.FloatField(default=0)
    min_score = models.FloatField(default=0)
    name = models.CharField(max_length=100, verbose_name="考试名称")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

class ApriExam(mongoengine.Document):
    exam_id = mongoengine.IntField()
    apri_res = mongoengine.StringField()


