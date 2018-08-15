# -*- coding: utf-8 -*-
import qiniu

from django.conf import settings
from qiniu import Auth

# TODO:

POLICY = settings.FILE_CALLBACK_POLICY or {
    'callbackUrl': settings.FILEUPLOAD_CALLBACK_URL,
    'callbackBody': 'bucket=$(bucket)&key=$(key)&filename=$(fname)&filesize=$(fsize)',
    'insertOnly': 1,
}


class UploadHandler(object):

    def __init__(self, key, secret, bucket):
        self.key = key
        self.secret = secret
        self.bucket = bucket
        self.backend = qiniu
        self._backend_auth = Auth(self.key, self.secret)

    def _upload_token(self, key, expires=3600, policy=None):
        token = self._backend_auth.upload_token(self.bucket, key=key, expires=expires, policy=policy)
        return token

    def upload_file(self, key, data, policy=None, fname='file_name'):
        if policy is None:
            policy = POLICY
        uptoken = self._upload_token(key, policy=policy)
        return self.backend.put_data(uptoken, key, data, fname=fname)

    def get_download_url(self, key):
        return '{}{}'.format(settings.FILE_DOWNLOAD_PREFIX, key)


upload_handler = None

if settings.FILE_UPLOAD_BACKEND == 'qiniu':
    upload_handler = UploadHandler(
        settings.FILE_UPLOAD_KEY,
        settings.FILE_UPLOAD_SECRET,
        settings.FILE_UPLOAD_BUCKET
    )
