# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from model_utils.models import TimeStampedModel


class UploadedFile(TimeStampedModel):
    user_id = models.PositiveIntegerField()
    bucket = models.CharField(blank=True, default='', max_length=64)
    name = models.CharField(blank=True, default='', max_length=255)
    filesize = models.CharField(blank=True, default='0', max_length=64)
    is_active = models.BooleanField(verbose_name=u'是否有效', default=False)

    class Meta:
        unique_together = (('bucket', 'name'),)
