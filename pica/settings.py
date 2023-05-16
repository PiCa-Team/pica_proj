"""
Django settings for pica project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
from datetime import datetime
from pathlib import Path
from config.environ import Environ
import pymysql
import os
from sshtunnel import SSHTunnelForwarder


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = Environ.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['3.37.204.249', 'localhost', '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "train_manage",
    "user",
    "core",
    "connect",
    "config",
    "django_crontab",

]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "pica.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "pica.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
pymysql.install_as_MySQLdb()

# SSH 터널 설정
server = SSHTunnelForwarder(
    (Environ.SSH_TUNNEL_HOST, Environ.SSH_TUNNEL_PORT),
    ssh_username=Environ.SSH_TUNNEL_USERNAME,
    ssh_pkey=Environ.SSH_TUNNEL_PKEY,
    remote_bind_address=(Environ.RDS_HOST, Environ.RDS_PORT)
)

server.start()  # SSH 터널 시작

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': Environ.RDS_DB_NAME,
        'USER': Environ.RDS_USERNAME,
        'PASSWORD': Environ.RDS_PASSWORD,
        'HOST': '127.0.0.1',
        'PORT': server.local_bind_port,  # 로컬 포트로 터널링된 포트 사용
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

TIME_ZONE = "Asia/Seoul"
USE_TZ = False

LANGUAGE_CODE = "ko-kr"
USE_I18N = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')


# Media Directory
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / 'media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# 로그인 URL
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'

# 사용자가 30분동안 활동이 없으면 자동으로 로그아웃
SESSION_COOKIE_AGE = 1800  # 1800 seconds = 30 minutes

# 슈퍼셋 설정
SUPERSET_URL = Environ.SUPERSET_URL
SUPERSET_USERNAME = Environ.SUPERSET_USERNAME
SUPERSET_PASSWORD = Environ.SUPERSET_PASSWORD

# date 설정
now = datetime.now()
formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")

CRONJOBS = [
    ('15 8,18 * * *',
     'train_manage.cron.cron_job',
     '>> '+os.path.join(BASE_DIR, f'config/cron_log/{formatted_date}.log')+' 2>&1 ')

    # ('*/2 * * * *',
    #  'train_manage.cron.cron_job',
    #  '>> '+os.path.join(BASE_DIR, f'config/cron_log/{datetime.now().date()}.log')+' 2>&1 ')


]