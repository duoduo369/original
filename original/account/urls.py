# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from .views import LoginView, LoginAPI, LogoutAPI
from .weaapp import WEAAPPAuthAPI, WEAAPPUserInfoAPI

api_urlpatterns = [
    url(r'^login/weaapp/$', WEAAPPAuthAPI.as_view(), name='login_weaapp'),
    url(r'^login/$', LoginAPI.as_view(), name='cms_login'),
    url(r'^logout/$', LogoutAPI.as_view(), name='logout'),
    url(r'^userinfo/weaapp/$', WEAAPPUserInfoAPI.as_view(), name='weaapp_userinfo'),
]

html_urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
]

urlpatterns = [
    url(r'^api/v1/', include(api_urlpatterns, namespace='api.v1')),
    url(r'', include(html_urlpatterns, namespace='html.v1')),
]
