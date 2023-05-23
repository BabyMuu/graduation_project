""" @File   : serialize
    @Author : BabyMuu
    @Time   : 2022/3/24 0:01
"""
from hashlib import md5

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from . import models as my_models
from gra.utils.encrypt import encryption

class UserSerializer(serializers.ModelSerializer):
    classes = serializers.CharField(max_length=200, write_only=True)
    name = serializers.CharField(max_length=50, write_only=True)

    class Meta:
        model = my_models.Users
        fields = [
            'id',
            'password',
            'username',
            'telephone',
            'types',
            'classes',
            'name'
        ]
        extra_kwargs = {
            'username': {'max_length': 18, 'min_length': 2},
            'password': {'max_length': 64, 'min_length': 6},
        }

    def validate(self, attrs):
        classes = ','.join(list(set(attrs['classes'].split(','))))
        self.context['classes'] = classes
        self.context['name'] = attrs['name']

        del attrs['classes'], attrs['name']

        return attrs

    def create(self, validated_data):
        user = my_models.Users.objects.create_user(**validated_data)
        self.context['id'] = user.id
        del user.id
        return user

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = my_models.Students
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = my_models.Teachers
        fields = '__all__'

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = my_models.Scores
        fields = ["id",
                  "score",
                  "student_id",
                  "stu_name",
                  "exam_id",
                  "score_situation",
                  "score_know_situation"
                  ]

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = my_models.Questions
        fields = '__all__'

class AccountSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=20)

    def validate(self, attrs):
        # 获取 user
        user = self._get_user(attrs)
        # 放到 context 中 , 可以在视图函数中取出来
        user_name = self._get_detail(user)
        self.context['user'] = user
        self.context['name'] = user_name
        return attrs

    @staticmethod
    def _get_user(attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = my_models.Users.objects.filter(username=username).first()
        if user:
            ret = user.check_password(password)
            if ret:
                return user
            else:
                raise ValidationError({'password': '密码错误'})
        raise ValidationError({'username': '用户名不存在'})

    def _get_detail(self, user):
        if user.types == my_models.Users.UserTypes.STUDENT:
            instance = my_models.Students.objects.get(user_id=user.id)
        else:
            instance = my_models.Teachers.objects.get(user_id=user.id)
        return instance.name
