# -*- coding: utf-8 -*-
import os

from .common import *

DEBUG = False
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
        'PORT': os.environ.get('ORIGINAL_MYSQL_PORT', 3306)
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

if os.path.isfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'private_production.py')):
    from .private_production import *  # pylint: disable=import-error,wildcard-import
