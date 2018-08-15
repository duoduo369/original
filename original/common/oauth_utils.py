# -*- coding: utf-8 -*-
import arrow

from django.conf import settings
from oauthlib import common
from oauth2_provider.models import AccessToken, Application


def generate_access_token(user):
    '''获取 accesstoken, 由于微信小程序无法使用session, 所以采用oauth的机制'''
    application = Application.objects.get(
        client_id=settings.ORIGINAL_OAUTH2_CLIENT_ID,
        client_secret=settings.ORIGINAL_OAUTH2_CLIENT_SECRET,
    )
    expires = arrow.now().shift(years=1).datetime
    token = common.generate_token()
    scopes = ['read', 'write']
    access_token = AccessToken(
        user=user,
        scope=scopes,
        expires=expires,
        token=token,
        application=application,
        source_refresh_token=None,
    )
    access_token.save()
    return access_token
