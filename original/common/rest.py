# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging

from django.conf import settings
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.http import Http404
from django.utils import six
from django.utils.translation import ugettext_lazy as _

from django_validator.exceptions import ValidationError
from rest_framework import status, exceptions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.exceptions import PermissionDenied as RestPermissionDenied, AuthenticationFailed, NotAuthenticated
from rest_framework.response import Response

from . import exceptions as custom_exceptions
from .exceptions import ErrorCode

logger = logging.getLogger(__name__)


def ErrorResponse(err_code=ErrorCode.system_error, message=u'Internal Server Error',
                  status=status.HTTP_400_BAD_REQUEST, headers=None):
    err = {
        'error_code': err_code,
        'message': message,
    }
    return Response(err, status, headers=headers)


class Error(Exception):

    def __init__(self, err_code, message=u'服务器异常', status_code=status.HTTP_400_BAD_REQUEST):
        self.err_code = err_code
        self.message = message
        self.status_code = status_code

    def __unicode__(self):
            return u'[Error] {}: {}({})'.format(self.err_code, self.message, self.status_code)

    def get_response(self):
        return ErrorResponse(self.err_code, self.message, self.status_code)


def exception_handler(exc, context):
    # cycle import
    from rest_framework.views import set_rollback

    if settings.DEBUG:
        logger.debug(exc, exc_info=1)

    if isinstance(exc, custom_exceptions.APIException):
        set_rollback()
        return ErrorResponse(
            err_code=exc.code,
            message=exc.message,
            status=status.HTTP_400_BAD_REQUEST
        )

    if isinstance(exc, Error):
        set_rollback()
        return exc.get_response()

    if isinstance(exc, (RestPermissionDenied, PermissionDenied)):
        msg = _('Permission denied.')
        data = {
            'detail': six.text_type(msg)
        }
        exc_message = str(exc)
        if 'CSRF' in exc_message:
            data['detail'] = exc_message

        set_rollback()
        return ErrorResponse(ErrorCode.permission_denied, u'您没有对应的权限', status=status.HTTP_403_FORBIDDEN)

    if isinstance(exc, ValidationError):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait
        error_code = ErrorCode.validator_error
        set_rollback()
        return ErrorResponse(error_code, exc.message)

    if isinstance(exc, NotAuthenticated):
        set_rollback()
        return ErrorResponse(ErrorCode.not_authenticated, u'您没有登陆')

    if isinstance(exc, AuthenticationFailed):
        set_rollback()
        return ErrorResponse(ErrorCode.authentication_failed, u'登陆失败，请稍后再试')

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
            show_message = data
        else:
            show_message = exc.detail
        set_rollback()
        return ErrorResponse(ErrorCode.api_exception, show_message, headers=headers)

    if isinstance(exc, Http404):
        set_rollback()
        return ErrorResponse(ErrorCode.not_found, u'404 not found', status=status.HTTP_404_NOT_FOUND)

    if isinstance(exc, ObjectDoesNotExist):
        set_rollback()
        return ErrorResponse(ErrorCode.not_found, u'404 not found: {}'.format(exc.__class__.__name__), status=status.HTTP_404_NOT_FOUND)

    logger.error(exc, exc_info=1)

    # Note: Unhandled exceptions will raise a 500 error.
    return None


class CSRFExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening
