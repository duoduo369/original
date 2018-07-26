# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.conf.urls import url
from .views import HeartBeatAPI

urlpatterns = [
    url(r'^heartbeat/$', HeartBeatAPI.as_view(), name='heartbeat'),
]
