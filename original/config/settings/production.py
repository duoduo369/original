# -*- coding: utf-8 -*-
import os

from .common import *

DEBUG = False
ENV_PREFIX = 'ORIGINAL'
# SECURITY WARNING: keep the secret key used in production secret!
# SECURITY WARNING: don't run with debug turned on in production!
SECRET_KEY = 'yb8tfe(b%4)leqm)!@b$w9b*gf6ub@_e#bi+(2^w7vk)!20cv!'

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('ORIGINAL_MYSQL_NAME', 'original'),
        'HOST': os.environ.get('ORIGINAL_MYSQL_HOST', 'localhost'),
        'USER': os.environ.get('ORIGINAL_MYSQL_USER', 'root'),
        'PASSWORD': os.environ.get('ORIGINAL_MYSQL_PASSWORD', None),
        'PORT': os.environ.get('ORIGINAL_MYSQL_PORT', 3306),
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(levelname)s %(process)d '
                      '[%(name)s] %(filename)s:%(lineno)d - %(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'stream': sys.stderr,
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        },
    }
}


def get_env_key(key):
    if not key:
        return ''
    return '{}_{}'.format(ENV_PREFIX, key)


SOCIAL_AUTH_WEIXIN_KEY = os.environ.get(get_env_key('SOCIAL_AUTH_WEIXIN_KEY'), '')
SOCIAL_AUTH_WEIXIN_SECRET = os.environ.get(get_env_key('SOCIAL_AUTH_WEIXIN_SECRET'), '')

SOCIAL_AUTH_WEIXINAPP_KEY = os.environ.get(get_env_key('SOCIAL_AUTH_WEIXINAPP_KEY'), '')
SOCIAL_AUTH_WEIXINAPP_SECRET = os.environ.get(get_env_key('SOCIAL_AUTH_WEIXINAPP_SECRET'), '')

WEAAPP_KEY = os.environ.get(get_env_key('WEAAPP_KEY'), '')
WEAAPP_SECRET = os.environ.get(get_env_key('WEAAPP_SECRET'), '')

FILE_UPLOAD_BACKEND = os.environ.get(get_env_key('FILE_UPLOAD_BACKEND'), '')
FILE_UPLOAD_KEY = os.environ.get(get_env_key('FILE_UPLOAD_KEY'), '')
FILE_UPLOAD_SECRET = os.environ.get(get_env_key('FILE_UPLOAD_SECRET'), '')
FILE_UPLOAD_BUCKET = os.environ.get(get_env_key('FILE_UPLOAD_BUCKET'), '')

FILEUPLOAD_CALLBACK_URL = os.environ.get(get_env_key('FILEUPLOAD_CALLBACK_URL'), '')
ORIGINAL_OAUTH2_CLIENT_ID = os.environ.get(get_env_key('ORIGINAL_OAUTH2_CLIENT_ID'), '')
ORIGINAL_OAUTH2_CLIENT_SECRET = os.environ.get(get_env_key('ORIGINAL_OAUTH2_CLIENT_SECRET'), '')

ENABLE_REDIS = os.environ.get(get_env_key('ENABLE_REDIS'), '0')
REDIS_HOST = os.environ.get(get_env_key('REDIS_HOST'), 'localhost')
REDIS_PORT = os.environ.get(get_env_key('REDIS_PORT'), 6379)
REDIS_DB = os.environ.get(get_env_key('REDIS_DB'), '0')

SMS_BACKEND = os.environ.get(get_env_key('SMS_BACKEND'), '')
SMS_QCLOUD_KEY = os.environ.get(get_env_key('SMS_QCLOUD_KEY'), '')
SMS_QCLOUD_SECRET = os.environ.get(get_env_key('SOCIAL_AUTH_WEIXINAPP_SECRET'), '')
SMS_QCLOUD_DEFAULT_TEMPLATE_ID = os.environ.get(get_env_key('SMS_QCLOUD_DEFAULT_TEMPLATE_ID'), '')

SMS_YUNPIAN_KEY = os.environ.get(get_env_key('SMS_YUNPIAN_KEY'), '')
SMS_YUNPIAN_SECRET = os.environ.get(get_env_key('SOCIAL_AUTH_WEIXINAPP_SECRET'), '')
SMS_YUNPIAN_DEFAULT_TEMPLATE_ID = os.environ.get(get_env_key('SMS_YUNPIAN_DEFAULT_TEMPLATE_ID'), '')

if os.path.isfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'private_production.py')):
    from .private_production import *  # pylint: disable=import-error,wildcard-import
