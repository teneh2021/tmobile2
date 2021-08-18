"""
Django settings for tmobile project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""


import platform
from pathlib import Path
import os
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
"""
usage:
platform.system()
platform.release()
os.name
The output of platform.system() is as follows:
Linux: Linux
Mac: Darwin
Windows: Windows
"""
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = os.path.join(BASE_DIR, 'tmobile/templates')
"""
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_ROOT = os.path.join(BASE_DIR, 'tmo_amara/')
MEDIA_URL= '/media/'
"""
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!
if platform.system()=="Windows":
    develop = True
elif platform.system()=="Linux":
    develop = False


if develop:
    SECRET_KEY = 'django-insecure--bju^8o$q48^5s3fe6&xu_zy25_-f39sb1sy-a7#hje(qpo)4g'
    DEBUG = True
    BASE_DIR = Path(__file__).resolve().parent.parent
    TEMPLATE_DIR = os.path.join(BASE_DIR, 'tmobile/templates')
    STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
    MEDIA_ROOT = os.path.join(BASE_DIR, 'tmo_amara/')
    MEDIA_URL = '/media/'
    STATIC_URL = '/static/'
    STATICFILES_DIR = [
        STATIC_ROOT,
    ]

else:

    SECRET_KEY = config('SECRET_KEY')
    DEBUG = config('DEGUG', default=False, cast=bool)

    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')  # raw spaces access key
    AWS_SECRET_ACCESS_KEY = config(
        'AWS_SECRET_ACCESS_KEY')  # raw spaces secret key
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_ENDPOINT_URL = config('AWS_S3_ENDPOINT_URL')
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_LOCATION = config('AWS_LOCATION')

    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'tmobile/static'),
    ]
    STATIC_URL = 'https://%s/%s/' % (AWS_S3_ENDPOINT_URL, AWS_LOCATION)
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


#AUTH_USER_MODEL = 'tmo_amara.User'
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tmo_amara',
    'widget_tweaks',
    'bootstrap_modal_forms',
    'chartjs',
    'storages',
    'django.contrib.humanize',
    'django_crontab',
    'django_cron',
    

]

CRONJOBS = [
    ('* * * * *', 'tmo_amara.cron.emailAlert')
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django_session_timeout.middleware.SessionTimeoutMiddleware', #for session timeout
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

ROOT_URLCONF = 'tmobile.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'tmobile.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


ALLOWED_HOSTS = ['localhost', '192.168.0.242', 'www.vangarmoh.com', 'vangarmoh.com']
DATABASES = {
'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
}
}

"""  
else:
    ALLOWED_HOSTS = ['206.189.191.246', 'localhost', 'www.vangarmoh.com', 'vangarmoh.com']
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
# Will learn how to user postgresql
 
else:
    ALLOWED_HOSTS = ['192.241.151.211', 'localhost']
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'tmobile',
            'USER': 'abc98',
            'PASSWORD': '1988',
            'HOST': 'localhost',
            'PORT': '',
        }
    }

"""

 

#AUTH_USER_MODEL = tmo_amara.User

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 4,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },

]

""" 
{
    'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
},
"""
# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

"""
STATIC_URL = '/static/'
STATICFILES_DIR =[
    STATIC_ROOT,
]
"""
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
#LOGIN_URL='/welcome'
#LOGIN_REDIRECT_URL ='/index'
LOGOUT_REDIRECT_URL = 'tmo_amara:login'

SILENCED_SYSTEM_CHECKS =['fields.W161']
SESSION_SAVE_EVERY_REQUEST=True
SESSION_COOKIE_SECURE=True
#SESSION_COOKIE_AGE = 20

#SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
#SESSION_EXPIRE_SECONDS =3

SESSION_SECURITY_EXPIRE_AFTER=360
SESSION_SECURITY_WARN_AFTER=350

SESSION_EXPIRE_AT_BROWSER_CLOSE=True