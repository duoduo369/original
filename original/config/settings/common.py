# -*- coding: utf-8 -*-
import sys
from os.path import join, abspath, dirname


# PATH vars
def root(*args):
    return join(abspath(join(dirname(__file__), '..', '..')), *args)


SECRET_KEY = 'insecure-secret-key'

DEBUG = False

ALLOWED_HOSTS = []

TESTING_MODE = False

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = (
    'rest_framework',
    'oauth2_provider',
    'social_django',
)

PROJECT_APPS = (
    'account',
    'misc',
)

INSTALLED_APPS = []
INSTALLED_APPS += DJANGO_APPS
INSTALLED_APPS += THIRD_PARTY_APPS
INSTALLED_APPS += PROJECT_APPS

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '' # TODO: FILL
STATICFILES_DIRS=(
    root('static'),
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            root('templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
            'debug': True,  # Django will only display debug pages if the global DEBUG setting is set to True
        },
    },
]


TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

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
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'stream': sys.stderr,
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'common.rest.CSRFExemptSessionAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'EXCEPTION_HANDLER': 'common.rest.exception_handler',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
}

AUTH_USER_MODEL = 'account.User'

TESTING_MODE = False

AUTHENTICATION_BACKENDS = (
    'social_core.backends.weixin.WeixinOAuth2',
    'social_core.backends.weixin.WeixinOAuth2APP',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'account.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'account.pipeline.social_auth.social_user_details',
    'account.pipeline.social_auth.create_user',
    'account.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

SOCIAL_AUTH_USER_MODEL = 'account.User'
SOCIAL_AUTH_UUID_LENGTH = 16

SOCIAL_AUTH_LOGIN_URL = '/login-url/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/logged-in/'
SOCIAL_AUTH_LOGIN_ERROR_URL = '/login-error/'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/new-users-redirect-url/'
SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/new-association-redirect-url/'
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/account-disconnected-redirect-url/'
SOCIAL_AUTH_INACTIVE_USER_URL = '/inactive-user/'

SOCIAL_AUTH_WEIXIN_KEY = ''
SOCIAL_AUTH_WEIXIN_SECRET = ''
SOCIAL_AUTH_WEIXIN_SCOPE = ['snsapi_login',]

SOCIAL_AUTH_WEIXINAPP_KEY = ''
SOCIAL_AUTH_WEIXINAPP_SECRET = ''
SOCIAL_AUTH_WEIXINAPP_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_WEIXINAPP_SCOPE = ['snsapi_userinfo',]

WEAAPP_KEY= ''
WEAAPP_SECRET= ''

FILE_UPLOAD_BACKEND = None # qiniu

FILE_UPLOAD_KEY = ''
FILE_UPLOAD_SECRET = ''
FILE_UPLOAD_BUCKET = ''
FILE_CALLBACK_POLICY = {}

FILEUPLOAD_CALLBACK_URL = ''
FILE_DOWNLOAD_PREFIX = ''
ORIGINAL_OAUTH2_CLIENT_ID = ''
ORIGINAL_OAUTH2_CLIENT_SECRET = ''
