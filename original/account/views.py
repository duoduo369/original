# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.views.generic.base import TemplateView
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


class LoginView(TemplateView):

    template_name = 'account/login.html'
