# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(db_index=True, blank=True, default='', max_length=150, verbose_name=u'用户名展示用')
    mobile = models.CharField(db_index=True, blank=True, default='', max_length=32, verbose_name=u'电话')
    email = models.EmailField(db_index=True, blank=True, default='',  max_length=64, verbose_name=u'邮箱')
    avatar = models.CharField(blank=True, max_length=255, default='', verbose_name=u'用户头像')


class SocialAuthUnionID(models.Model):
    '''微信需要使用这个东西'''
    provider = models.CharField(max_length=32)
    uid = models.CharField(max_length=255)
    unionid = models.CharField(max_length=255, db_index=True, default='')

    class Meta:
        unique_together = (('provider', 'uid', 'unionid'),)
