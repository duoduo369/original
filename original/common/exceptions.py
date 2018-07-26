# -*- coding: utf-8 -*-
from __future__ import absolute_import


class ErrorCode(object):
    system_error = 10001

    missing_parameter = 20001
    invalid_parameter = 20002
    api_exception = 20003
    not_found = 20004
    not_authenticated = 20005
    permission_denied = 20006
    authentication_failed = 20007
    serializer_error = 20008

    validator_error = 30000


class BaseException(Exception):

    def __init__(self, code=ErrorCode.system_error, message=''):
        self.code = code
        self.message = message
        super(Exception, self).__init__(unicode(self))

    def __unicode__(self):
        return u'[Exception] code: {}, message: {}'.format(self.code, self.message)


class APIException(BaseException):
    pass


class APISerializerException(APIException):
    def __init__(self, code=ErrorCode.serializer_error, message='SerializerError'):
        super(APISerializerException, self).__init__(code=code, message=message)


class APIPermissionDeniedException(APIException):
    def __init__(self, code=ErrorCode.permission_denied , message='PermissionDenied'):
        super(APIPermissionDeniedException, self).__init__(code=code, message=message)


class APINotFoundException(APIException):

    def __init__(self, code=ErrorCode.not_found, message='not found'):
        super(APINotFoundException, self).__init__(code=code, message=message)


class APIParamException(APIException):

    def __init__(self, code=ErrorCode.invalid_parameter, message='invalid_parameter'):
        super(APIParamException, self).__init__(code=code, message=message)
