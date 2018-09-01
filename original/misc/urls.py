# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from .views import FileUploadAPI, FileUploadCallBackAPI, SignedJSConfig
from . import validation

api_urlpatterns = [
    url(r'^file/upload/$', FileUploadAPI.as_view(), name='file_upload'),
    url(r'^file/upload/callback/$', FileUploadCallBackAPI.as_view(), name='file_upload_callback'),
    url(r'^validation/$', validation.validate_image, name='get_validate_image'),
]

urlpatterns = [
    url(r'^api/v1/', include(api_urlpatterns, namespace='api.v1')),
]
