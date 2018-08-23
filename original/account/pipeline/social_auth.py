# -*- coding: utf-8 -*-
import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from social_core.exceptions import AuthAlreadyAssociated

from ..models import SocialAuthUnionID

User = get_user_model()

log = logging.getLogger(__name__)


def social_user_details(backend, details, response, *args, **kwargs):
    # name for show
    name = details['username']
    # username is uuid for unique
    username = kwargs['username']
    profile_image_url = details['profile_image_url']
    uid = kwargs['uid']
    unionid = kwargs.get('unionid')
    return {
        'name': name,
        'username': username,
        'profile_image_url': profile_image_url,
        'uid': uid,
        'unionid': unionid,
    }

def social_user(backend, uid, user=None, *args, **kwargs):
    provider = backend.name
    unionid = kwargs.get('unionid')
    social = backend.strategy.storage.user.get_social_auth(provider, uid)
    # 如果这个uid未能找到, 需要查看他关联的unionid
    # 是否有其他微信使用
    if not social and unionid:
        social_auth_unionids = SocialAuthUnionID.objects.filter(unionid=unionid)
        for each in social_auth_unionids:
            if each.uid == uid and each.provider == provider:
                continue
            social = backend.strategy.storage.user.get_social_auth(each.provider, each.uid)
            if social:
                break
    if social:
        if user and social.user != user:
            msg = 'This {0} account is already in use.'.format(provider)
            raise AuthAlreadyAssociated(backend, msg)
        elif not user:
            user = social.user
    return {'social': social,
            'user': user,
            'is_new': user is None,
            'new_association': social is None}


def create_user(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}

    USER_FIELDS = ['username', 'name', 'profile_image_url', 'uid', 'uuid']

    fields = dict((name, kwargs.get(name, details.get(name)))
                  for name in backend.setting('USER_FIELDS', USER_FIELDS))
    if not fields:
        return
    if settings.DEBUG:
        log.debug(details)
        log.debug(args)
        log.debug(kwargs)
    user = User(
        username=fields['username'], name=fields['name'], avatar=fields['profile_image_url']
    )
    user.set_unusable_password()
    user.save()

    return {
        'is_new': True,
        'user': user,
    }


def associate_user(backend, uid, user=None, social=None, *args, **kwargs):
    if user and not social:
        unionid = kwargs.get('unionid', '') or ''
        SocialAuthUnionID.objects.get_or_create(provider=backend.name, uid=uid, unionid=unionid)
        try:
            social = backend.strategy.storage.user.create_social_auth(
                user, uid, backend.name
            )

        except Exception as err:
            if not backend.strategy.storage.is_integrity_error(err):
                raise
            # Protect for possible race condition, those bastard with FTL
            # clicking capabilities, check issue #131:
            #   https://github.com/omab/django-social-auth/issues/131
            return social_user(backend, uid, user, *args, **kwargs)
        else:
            return {'social': social,
                    'user': social.user,
                    'new_association': True}
