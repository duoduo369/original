#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import logging
import random
import requests
import string
import time
import json

from django.conf import settings
from django.core import cache

log = logging.getLogger(__name__)

try:
    cache = cache.get_cache('general')
except Exception:
    cache = cache.cache


class Sign:
    def __init__(self, jsapi_ticket, url):
        self.ret = {
            'nonceStr': self.__create_nonce_str(),
            'jsapi_ticket': jsapi_ticket,
            'timestamp': self.__create_timestamp(),
            'url': url
        }

    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def __create_timestamp(self):
        return int(time.time())

    def sign(self):
        string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
        self.ret['signature'] = hashlib.sha1(string).hexdigest()
        return self.ret


def get_weixin_accesstoken(key, secret):
    cache_key = 'weixinapp_access_token:{}'.format(key)
    access_token = cache.get(cache_key)
    if access_token:
        return access_token
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(key, secret)
    try:
        log.info('try get weixin access_token from wechat server')
        response = requests.get(url).json()
    except Exception as ex:
        log.info(ex)
        return ''
    access_token = response.get('access_token')
    expires_in = response.get('expires_in')
    if access_token and expires_in:
        expires_in = int(expires_in)
        cache.set(cache_key, access_token, int(expires_in/4.0*3))
        log.info('cache weixin access_token, key: %s, ticket: %s', cache_key, access_token)
        return access_token
    log.warning(response)
    return ''


def get_weixin_user_info(access_token, openid):
    url = 'https://api.weixin.qq.com/cgi-bin/user/info?access_token={}&openid={}&lang=zh_CN'.format(
        access_token,
        openid
    )
    try:
        response = requests.get(url).json()
        return response
    except Exception as ex:
        log.info(ex)
        return {}


def get_jsapi_ticket(key, secret):
    cache_key = 'weixinapp_jsapi_ticket:{}'.format(key)
    ticket = cache.get(cache_key)
    if ticket:
        return ticket
    access_token = get_weixin_accesstoken(key, secret)
    url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={}&type=jsapi'.format(
            access_token
    )
    try:
        log.info('try get weixin ticket from wechat server')
        response = requests.get(url).json()
    except Exception as ex:
        log.info(ex)
        return ''
    ticket = response.get('ticket')
    expires_in = response.get('expires_in')
    if ticket:
        expires_in = int(expires_in)
        cache.set(cache_key, ticket, int(expires_in/4.0*3))
        log.info('cache weixin ticket, key: %s, ticket: %s', cache_key, ticket)
        return ticket
    log.warning(response)
    return ''


def get_signed_js_config(url, key, secret):
    sign = Sign(get_jsapi_ticket(key, secret), url)
    return sign.sign()


def send_template_message(access_token, openid, template_id, form_id='FORMID', data=None):
    '''https://developers.weixin.qq.com/miniprogram/dev/api/notice.html#%E6%A8%A1%E7%89%88%E6%B6%88%E6%81%AF%E7%AE%A1%E7%90%86'''
    data = data or {}
    for key in data.keys():
        value = data[key]
        value['value'] = unicode(value['value']).encode('utf-8')

    url = 'https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token={}'.format(access_token)
    params = {
        'touser': openid,
        'template_id': template_id,
        'form_id': form_id,
        'data': data,
    }
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(params), headers=headers).json()
    except Exception as ex:
        log.error(ex)
    log.info(response)
