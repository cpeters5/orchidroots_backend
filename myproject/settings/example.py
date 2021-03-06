from __future__ import absolute_import, unicode_literals

from .base import *

import os

DEBUG = True

ALLOWED_HOSTS = []


# ALLOWED_HOSTS = [
#     'orchidroots.org',
#     'www.orchidroots.org',
#     '134.209.93.40',
#     '127.0.0.1',
#     'localhost',
# ]

SYS_ADMINS = ['ibrahim@excelcodes.com']

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = ''
SKIP_SENDING_EMAIL = False

# Database Local
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Database Live
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'stage1',
#         'HOST': '167.172.24.44',
#         'USER':'dbuser',
#         'PASSWORD':'Imh#r3r3',
#     }
# }

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}


FACEBOOK_CLIENT_ID = ''
FACEBOOK_CLIENT_SECRET = ''