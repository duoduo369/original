# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from .views import (
    FileUploadAPI, FileUploadCallBackAPI, SignedJSConfig,
    SMSAPI, SMSCheckAPI
)
from . import validation

api_urlpatterns = [
    url(r'^file/upload/$', FileUploadAPI.as_view(), name='file_upload'),
    url(r'^file/upload/callback/$', FileUploadCallBackAPI.as_view(), name='file_upload_callback'),
    url(r'^signed_js_config/$', SignedJSConfig.as_view(), name='signed_js_config'),
    url(r'^validation/$', validation.validate_image, name='get_validate_image'),
    url(r'^sms/$', SMSAPI.as_view(), name='send_sms'),
    url(r'^sms/check/$', SMSCheckAPI.as_view(), name='send_check'),
]

urlpatterns = [
    url(r'^api/v1/', include(api_urlpatterns, namespace='api.v1')),
]
