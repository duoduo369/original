# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
import logging
import json

from django.conf import settings
from django.core import cache
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django_validator.decorators import GET, POST
from common import constants, exceptions, weixin
from common.upload import upload_handler

from common.sms import sms_handler
from .models import UploadedFile
from .models import (
    SMS_OUT_OF_DATE, SMS_TOO_FREQUENTLY, SMS_VERIFICATION_FAILED,
    SMS_VERIFICATION_SUCCESS, SMS_WAIT_TO_CHECK, SMSValidate,
    SMS_SEND_FAILED, SMSValidateCheckFailures, SMS_OUT_DAILY_NUMBER_LIMIT
)

try:
    cache = cache.get_cache('general')
except Exception:
    cache = cache.cache

log = logging.getLogger(__name__)


class FileUploadAPI(APIView):

    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user_id = request.user.id
        file_obj = request.data['file']
        file_name = file_obj.name
        file_type = file_name.split('.')[-1]
        upload_file_name = '{}.{}'.format(uuid.uuid4().hex[:16], file_type)
        bucket = settings.FILE_UPLOAD_BUCKET
        _file, _created = UploadedFile.objects.get_or_create(
            bucket=bucket, name=upload_file_name, defaults={
                'user_id': user_id,
                'filesize': 0,
        })
        if not _created:
            _file.user_id = user_id
            _file.save()
        resp = upload_handler.upload_file(upload_file_name, file_obj)
        data = {
            'data': {
                'id': _file.id,
                'url': upload_handler.get_download_url(upload_file_name),
                'is_active': _file.is_active,
            }
        }
        return Response(data)


class FileBase64UploadAPI(APIView):

    permission_classes = (IsAuthenticated,)

    @POST('base64_file', type='str', validators='required')
    def post(self, request, base64_file):
        user_id = request.user.id
        customer_id = request.user.customer_id
        base64_prefix, image_data = base64_file.split(',')
        decode_file = base64.b64decode(image_data)
        file_obj = StringIO.StringIO(decode_file)
        # base64_prefix like 'data:image/png;base64'
        file_type = base64_prefix.split('/')[1].split(';')[0]
        upload_file_name = '{}.{}'.format(uuid.uuid4().hex[:16], file_type)
        bucket = settings.FILE_UPLOAD_BUCKET
        _file, _created = UploadedFile.objects.get_or_create(
            bucket=bucket, name=upload_file_name, defaults={
                'user_id': user_id,
                'customer_id': customer_id,
                'filesize': 0,
        })
        if not _created:
            _file.user_id = user_id
            _file.save()
        resp = upload_handler.upload_file(upload_file_name, file_obj)
        data = {
            'data': {
                'id': _file.id,
                'url': upload_handler.get_download_url(upload_file_name),
                'is_active': _file.is_active,
            }
        }
        return Response(data)


class FileUploadCallBackAPI(APIView):

    @POST('bucket', type='str', default='')
    @POST('key', type='str', default='')
    @POST('filename', type='str', default='')
    @POST('filesize', type='str', default='')
    def post(self, request, bucket, key, filename, filesize):
        _file, _created = UploadedFile.objects.get_or_create(
            bucket=bucket, name=key, defaults={
                'user_id': 0,
                'filesize': filesize,
                'is_active': True,
        })
        if not _created:
            _file.filesize = filesize
            _file.is_active = True
            _file.save()
        return Response()


class SignedJSConfig(APIView):

    @GET('url', type='str', validators='required')
    def get(self, request, url):
        appid = settings.SOCIAL_AUTH_WEIXINAPP_KEY
        appsecret = settings.SOCIAL_AUTH_WEIXINAPP_SECRET
        config = weixin.get_signed_js_config(url, appid, appsecret)
        return Response(config)


class SMSAPI(APIView):

    @POST('phone_number', type='str', validators='required')
    @POST('verify', type='str', validators='required')
    def post(self, request, phone_number, verify):
        captcha = verify
        verify = request.session.get(constants.VALIDATION_SESSION_KEY, '')
        request.session[constants.VALIDATION_SESSION_KEY] = '!'
        if not captcha or verify.lower() != captcha.lower():
            raise exceptions.APIValidationCodeException(message=u'验证码错误')
        cache_key = 'sms_{}'.format(phone_number)
        phone_number_cached = cache.get(cache_key, None)
        if phone_number_cached:
            raise exceptions.APISMSException(
                code=exceptions.ErrorCode.sms_too_frequently, message=u'验证码请求过于频繁'
            )
        else:
            cache.set(cache_key, 1, SMSValidate.FREQUENTLY_TIME-1)

        if SMSValidate.is_out_of_limit(phone_number):
            raise exceptions.APISMSException(
                code=exceptions.ErrorCode.sms_out_daily_number_limit,
                message=u'手机号验证码达到当日上限'
            )

        sms_list = SMSValidate.objects.filter(status=SMS_WAIT_TO_CHECK, phone_number=phone_number).order_by('-created_at')
        # 防止用户恶意注册
        if sms_list.exists():
            sms_obj = sms_list[0]
            if sms_obj.is_too_frequently():
                raise exceptions.APISMSException(
                    code=exceptions.ErrorCode.sms_too_frequently, message=u'验证码请求过于频繁'
                )
        try:
            obj = SMSValidate.new(phone_number)
        except Exception as ex:
            log.warning(ex, exc_info=1)
            raise exceptions.APISMSException()
        sms_handler.send_with_template(
            phone_number, settings.SMS_QCLOUD_DEFAULT_TEMPLATE_ID,
            template_params=[obj.validate, str(SMSValidate.EXPIRE_TIME / 60)]
        )
        return Response()


class SMSCheckAPI(APIView):

    @POST('phone_number', type='str', validators='required')
    @POST('validate', type='str', validators='required')
    def post(self, request, phone_number, verify):
        status = SMSValidate.check_validate(phone_number, validate)
        if status == SMS_VERIFICATION_SUCCESS:
            SMSValidateCheckFailures.clear_lockout_counter(phone_number)
        else:
            SMSValidateCheckFailures.increment_lockout_counter(phone_number)
            raise exceptions.APISMSException(code=exceptions.ErrorCode.sms_check_failed, message=u'验证码错误')
        return Response()
