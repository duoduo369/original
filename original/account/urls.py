# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from .views import LoginView

api_urlpatterns = []

html_urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
]

urlpatterns = [
    url(r'^api/v1/', include(api_urlpatterns, namespace='api.v1')),
    url(r'', include(html_urlpatterns, namespace='html.v1')),
]
