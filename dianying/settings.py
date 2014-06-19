#coding:utf-8
"""
Django settings for dianying project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import deploy_settings
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = deploy_settings.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = deploy_settings.DEBUG

TEMPLATE_DEBUG = deploy_settings.DEBUG

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django.contrib.humanize",
    'MyUser',
    'nanjing',
    'pagination',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "template"),
)

TEMPLATE_CONTEXT_PROCESSORS = (
     'django.contrib.auth.context_processors.auth',
     'django.core.context_processors.debug',
     'django.core.context_processors.i18n',
     'django.core.context_processors.media',
     'django.core.context_processors.request',
     'django.core.context_processors.static',
     'django.core.context_processors.tz',
     'django.contrib.messages.context_processors.messages',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pagination.middleware.PaginationMiddleware'
)

ROOT_URLCONF = 'dianying.urls'

WSGI_APPLICATION = 'dianying.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',					 # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': deploy_settings.MYSQL_DB,                        # Or path to database file if using sqlite3.
        														 # The following settings are not used with sqlite3:
        'USER':deploy_settings.MYSQL_USER,
        'PASSWORD': deploy_settings.MYSQL_PASS,
        'HOST': deploy_settings.MYSQL_HOST,                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': deploy_settings.MYSQL_PORT,                      # Set to empty string for default.
        'CONN_MAX_AGE': 61                                    #None for unlimited persistent connections
    }
 }

# CACHES = {
#     default:{
#         'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
#         'LOCATION': 'CacheView',
#     }
# }
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '/static/')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static').replace("\\", '/'),)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media").replace('\\', '/')

MAX_UPLOAD_SIZE = "2560"

CONN_MAX_AGE = 10

#自定义用户模型
AUTH_USER_MODEL = 'MyUser.MyUser'

AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)


# 修改上传时文件在内存中可以存放的最大size为10m
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760


#if deploy_settings.DEFAULT_FILE_STORAGE:
    # sae的本地文件系统是只读的，修改django的file storage backend为Storage
    #DFAULT_FILE_STORAGE = deploy_settings.DEFAULT_FILE_STORAGE
    # 使用media这个bucket
    #STORAGE_BUCKET_NAME = 'media'
    # ref: https://docs.djangoproject.com/en/dev/topics/files/


