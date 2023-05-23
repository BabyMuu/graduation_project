"""
Django settings for BE project.

Generated by 'django-admin startproject' using Django 4.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PRJAPI_PATH = os.path.join(BASE_DIR, "gra")
APPS_DIR = os.path.join(BASE_DIR, "gra", "apps")
sys.path.append(PRJAPI_PATH)
sys.path.append(APPS_DIR)

# Build paths inside the project like this: BASE_DIR / 'subdir'.

STATIC_URL = '/static/'
MEDIA_URL = 'media/'
AUTH_USER_MODEL = 'user.Users'
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-vsjud041%vlxop7xz+5d06^7m%c^&o@$hi^pwo-bc+!8bi_lz)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 跨域
    "corsheaders",

    # drf
    'rest_framework',
    'rest_framework_jwt',
    'django_filters',

    # 子应用
    'user.apps.UserConfig',
    "analysis.apps.AnalysisConfig",
]
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 新加
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',  # 新加
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'BE.urls'

TEMPLATES = [
    {
        'BACKEND' : 'django.template.backends.django.DjangoTemplates',
        'DIRS'    : [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS' : {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'BE.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE'  : "django.db.backends.mysql",
        'NAME'    : "gra",  # 连接数据库名称
        "USER"    : "root",  # 数据库用户名
        "PASSWORD": "123456",  # 数据库密码
        "HOST"    : "127.0.0.1",  # 连接主机
        "PORT"    : 3306  # 端口号 默认 3306
    },
    "mangodb": {
        'ENGINE': None
    }
}

# 连接 MongoDB
from mongoengine import connect

connect('gra_ana')
# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

# 国际化 切换为中文
LANGUAGE_CODE = 'zh-hans'
# 时区
TIME_ZONE = 'Asia/shanghai'
# celery 时区问题
CELERY_ENABLE_UTC = False
DJANGO_CELERY_BEAT_TZ_AWARE = False

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_CREDENTIALS = True  # 允许跨域时携带Cookie，默认为False
CORS_ORIGIN_ALLOW_ALL = True  # 所有ip都可以访问后端接口
CORS_ORIGIN_WHITELIST = ["http://127.0.0.1:8000", "http://locolhost:8000"]  # 指定能够访问后端接口的ip或域名列表

# 允许访问的请求方法
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

# 允许的headers
CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)
