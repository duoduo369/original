# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from .views import LoginView
from .weaapp import WEAAPPAuthView, WEAAPPUserInfoView

api_urlpatterns = [
    url(r'^login/weaapp/$', WEAAPPAuthView.as_view(), name='login_weaapp'),
    url(r'^userinfo/weaapp/$', WEAAPPUserInfoView.as_view(), name='weaapp_userinfo'),
]

html_urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
]

urlpatterns = [
    url(r'^api/v1/', include(api_urlpatterns, namespace='api.v1')),
    url(r'', include(html_urlpatterns, namespace='html.v1')),
]
