# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
import logging
from django.conf import settings
from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django_validator.decorators import POST
from common.upload import upload_handler
from .models import UploadedFile

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
