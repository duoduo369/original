# -*- coding: utf-8 -*-
import logging
import urllib

from django.conf import settings
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
from yunpian_python_sdk.model import constant as YC
from yunpian_python_sdk.ypclient import YunpianClient

from . import exceptions

logger = logging.getLogger(__name__)


class QCloudSMSHandler(object):

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret
        self.sender = SmsSingleSender(key, secret)

    def send_with_template(self, phone_number, template_id, template_params=None, sms_sign=''):
        '''
        https://pypi.org/project/qcloudsms-py/
        result example
        {
            u'errmsg': u'OK',
            u'ext': u'',
            u'fee': 1,
            u'result': 0,
            u'sid': u'8:aa8Uti3rcuz968AlQFy20180901'
        }
        '''
        template_params = template_params or []
        try:
            result = self.sender.send_with_param(
                86, phone_number, template_id, template_params, sign=sms_sign, extend='', ext=''
            )
        except Exception as ex:
            log.warning(ex, exc_info=1)
            raise exceptions.APISMSException(message=ex)
        if result['result'] != 0:
            raise exceptions.APISMSException(message=result)
        return result


class YunPianSMSHandler(object):

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret
        self.client = YunpianClient(apikey=key)
        self.sender = self.client.sms()

    def send_with_template(self, phone_number, template_id, template_params=None, sms_sign=''):
        '''
        https://github.com/yunpian/yunpian-python-sdk
        https://www.jianshu.com/p/b2c1944c8b27
        '''
        template_params = template_params or {}
        if template_params:
            _params = {'#{}#'.format(key): value.encode('utf-8') for key, value in template_params.iteritems()}
            tpl_value = urllib.urlencode(_params)
        else:
            tpl_value = ''
        params = {
            YC.MOBILE: phone_number,
            YC.TPL_ID: int(template_id),
            YC.TPL_VALUE: tpl_value
        }
        result = self.sender.tpl_single_send(params)
        if result.code() != 0:
            raise exceptions.APISMSException(message=u'{}:{}'.format(result.code(), result.msg()))
        return result


sms_handler = None


if settings.SMS_BACKEND == 'qcloud':
    sms_handler = QCloudSMSHandler(
        settings.SMS_QCLOUD_KEY,
        settings.SMS_QCLOUD_SECRET,
    )
elif settings.SMS_BACKEND == 'yunpian':
    sms_handler = YunPianSMSHandler(
        settings.SMS_YUNPIAN_KEY,
        settings.SMS_YUNPIAN_SECRET,
    )
