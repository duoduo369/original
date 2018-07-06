# -*- coding: utf-8 -*-
import os

from .common import *

DEBUG = True

ALLOWED_HOSTS = ['*']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': root('..', 'db.sqlite3'),
    }
}

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(root(), "media")
INSTALLED_APPS += [
    'quickdev',
]

#####################################################################
# Lastly, see if the developer has any local overrides.
if os.path.isfile(join(dirname(abspath(__file__)), 'private.py')):
    from .private import *  # pylint: disable=import-error,wildcard-import
