# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic.base import TemplateView
from django.shortcuts import render


class LoginView(TemplateView):

    template_name = 'account/login.html'
