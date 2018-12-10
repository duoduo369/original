# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from .views import (
    FileUploadAPI, FileBase64UploadAPI, FileUploadCallBackAPI, SignedJSConfig,
    SMSAPI, SMSCheckAPI, CallBackCCLiveStartAPI, CallBackCCLiveEndAPI,
    CallBackCCRecordAPI, CallBackCCOfflineWatchAPI, CCAuthAPI,
)
from . import validation

api_urlpatterns = [
    url(r'^file/upload/$', FileUploadAPI.as_view(), name='file_upload'),
    url(r'^file/upload/base64/$', FileBase64UploadAPI.as_view(), name='file_base64_upload'),
    url(r'^file/upload/callback/$', FileUploadCallBackAPI.as_view(), name='file_upload_callback'),
    url(r'^signed_js_config/$', SignedJSConfig.as_view(), name='signed_js_config'),
    url(r'^validation/$', validation.validate_image, name='get_validate_image'),
    url(r'^sms/$', SMSAPI.as_view(), name='send_sms'),
    url(r'^sms/check/$', SMSCheckAPI.as_view(), name='send_check'),
    url(r'^cc/auth/$', CCAuthAPI.as_view(), name='cc_auth'),
    url(r'^callback/cc/live/start/$', CallBackCCLiveStartAPI.as_view(), name='callback_cc_live_start'),
    url(r'^callback/cc/live/end/$', CallBackCCLiveEndAPI.as_view(), name='callback_cc_live_end'),
    url(r'^callback/cc/record/$', CallBackCCRecordAPI.as_view(), name='callback_cc_record'),
    url(r'^callback/cc/offline/watch/$', CallBackCCOfflineWatchAPI.as_view(), name='callback_cc_offline_watch'),
]

urlpatterns = [
    url(r'^api/v1/', include(api_urlpatterns, namespace='api.v1')),
]
