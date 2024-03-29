"""
Django settings for eventaraAPI project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import environ

env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG_VALUE') == 'True'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME') or 'MyDatabase',
        'USER': os.getenv('DB_USER') or 'root',
        'PASSWORD': os.getenv('DB_PASSWORD') or '',
        'HOST': os.getenv('DB_HOST') or 'localhost',
        'PORT': os.getenv('DB_PORT') or '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'use_unicode': True,
        }
    }
}


ALLOWED_HOSTS = ['*'] 


AUTH_USER_MODEL = 'accounts.Account'
AUTHENTICATION_BACKENDS = (
    'accounts.models.UsernameOrEmailBackend', # our custom authentication backend
    'django.contrib.auth.backends.ModelBackend' # fallback to default authentication backend if first fails
    )
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'drf_yasg',
    'accounts',
    'categories',
    'events',
    'organizers',
    'jwttoken'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'eventaraAPI.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'eventaraAPI.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
    'NON_FIELD_ERRORS_KEY': 'Error',
    'TIME_FORMAT': "%H:%M",
}
#
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    }
}

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'id'

TIME_ZONE = 'Asia/Jakarta'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')


# Media Store in Bucket

credentials = f'''{{
    "type":"{os.getenv('type')}",
    "project_id":"{os.getenv('project_id')}",
    "private_key_id":"{os.getenv('private_key_id')}",
    "private_key":"{os.getenv('private_key')}",
    "client_email":"{os.getenv('client_email')}",
    "client_id":"{os.getenv('client_id')}",
    "auth_uri":"{os.getenv('auth_uri')}",
    "token_uri":"{os.getenv('token_uri')}",
    "auth_provider_x509_cert_url":"{os.getenv('auth_provider_x509_cert_url')}",
    "client_x509_cert_url":"{os.getenv('client_x509_cert_url')}",
}}'''

import ast
from google.oauth2 import service_account
GS_CREDENTIALS = service_account.Credentials.from_service_account_info(ast.literal_eval(credentials))


# Configuration for media file storing
DEFAULT_FILE_STORAGE = 'eventaraAPI.gcloud.GoogleCloudMediaFileStorage'
GS_PROJECT_ID = 'event-316818'
GS_BUCKET_NAME = 'eventara-images'
MEDIA_ROOT = 'media/'
UPLOAD_ROOT = 'media/uploads/'
MEDIA_URL = 'https://storage.googleapis.com/{}/'.format(GS_BUCKET_NAME)


# CORS Configuration
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


if DEBUG: 
   STATIC_ROOT = os.path.join(BASE_DIR, '/static')
else:
   STATIC_ROOT = os.path.join(BASE_DIR, 'static') 



# Mail Configuration
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False


# Frontend Configuration
FRONTEND_URL=os.getenv('FRONTEND_URL')