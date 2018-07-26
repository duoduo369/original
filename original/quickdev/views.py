# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


class HeartBeatAPI(APIView):

    def get(self, request):
        data = {'beat': 1}
        return Response(data)
