# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import TemplateView
from django.shortcuts import render
from django_validator.decorators import POST
from rest_framework.views import APIView
from rest_framework.response import Response
from common import exceptions


class LoginView(TemplateView):

    template_name = 'account/login.html'


class LoginAPI(APIView):

    @POST('username', type='string', validators='required')
    @POST('password', type='string', validators='required')
    def post(self, request, username, password):
        user = authenticate(username=username, password=password)
        if user is None:
            raise exceptions.APIPermissionDeniedException(message=u'用户名或密码错误')
        if not user.is_staff:
            raise exceptions.APIPermissionDeniedException(message=u'没有对应的权限')
        login(request, user)
        return Response()


class LogoutAPI(APIView):

    def get(self, request):
        logout(request)
        return Response()
