# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import redis

from django.conf import settings

redis_client = None

if settings.ENABLE_REDIS:
    redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
