# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import random
import uuid

from datetime import datetime, timedelta, date
from django.db import models
from django.utils import timezone
from model_utils.models import TimeStampedModel

from common import constants


class UploadedFile(TimeStampedModel):
    user_id = models.PositiveIntegerField()
    bucket = models.CharField(blank=True, default='', max_length=64)
    name = models.CharField(blank=True, default='', max_length=255)
    filesize = models.CharField(blank=True, default='0', max_length=64)
    is_active = models.BooleanField(verbose_name=u'是否有效', default=False)

    class Meta:
        unique_together = (('bucket', 'name'),)


# TODO: old code, need refactor
SMS_WAIT_TO_CHECK = 0
SMS_OUT_OF_DATE = 1
SMS_VERIFICATION_FAILED = 2
SMS_VERIFICATION_SUCCESS = 3
SMS_TOO_FREQUENTLY = 4
SMS_SEND_FAILED = 5
SMS_RECHECKED = 6
SMS_OUT_DAILY_NUMBER_LIMIT = 7


class SMSValidate(models.Model):
    '''
    phone_number: 用户手机号
    validate: 生成的验证码 6位即可
    status:
        0: 刚生成，待验证
        1: 验证码过期
        2: 验证失败
        3: 验证成功
        4: 发送频率过高
        5: 验证码发送失败
    created_at: 创建时间
    EXPIRE_TIME 过期时间 600秒
    '''
    STATUS = {
        SMS_WAIT_TO_CHECK: u'等待验证',
        SMS_OUT_OF_DATE: u'验证码已失效',
        SMS_VERIFICATION_FAILED: u'验证码错误',
        SMS_VERIFICATION_SUCCESS: u'验证成功',
        SMS_TOO_FREQUENTLY: u'验证码发送频率过高',
        SMS_SEND_FAILED: u'验证码发送失败',
        SMS_RECHECKED: u'验证码已失效',
        SMS_OUT_DAILY_NUMBER_LIMIT: u'同一手机号发送短信数量过多，请改天再来',
    }
    FREQUENTLY_TIME = 60
    EXPIRE_TIME = 600
    DAILY_NUMBER_LIMIT = 10
    VALIDATE_LENGTH = 6
    phone_number = models.CharField(max_length=20, db_index=True)
    validate = models.CharField(max_length=20, db_index=True)
    token = models.CharField(default='', max_length=255, db_index=True)
    status = models.PositiveSmallIntegerField(default=SMS_WAIT_TO_CHECK, db_index=True)
    request_date = models.DateField(default=None)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def new(cls, phone_number, token=''):
        now = datetime.now().date()
        obj = cls()
        obj.phone_number = phone_number
        obj.status = SMS_WAIT_TO_CHECK
        obj.validate = str(uuid.uuid4().int)[:cls.VALIDATE_LENGTH]
        obj.request_date = now
        obj.token = token
        obj.save()
        return obj

    def is_out_of_date(self):
        now = timezone.now()
        delta = now - self.created_at
        if delta.seconds >= self.EXPIRE_TIME:
            return True
        return False

    def is_too_frequently(self):
        now = timezone.now()
        delta = now - self.created_at
        if delta.seconds <= self.FREQUENTLY_TIME:
            return True
        return False

    @classmethod
    def is_out_of_limit(cls, phone_number):
        now = datetime.now().date()
        sms_list = cls.objects.filter(phone_number=phone_number, request_date=now)
        if sms_list.count() >= cls.DAILY_NUMBER_LIMIT:
            return True
        return False

    @classmethod
    def check_validate(cls, phone_number, validate):
        sms_list = cls.objects.filter(status=SMS_WAIT_TO_CHECK, phone_number=phone_number).order_by('-created_at')
        if not sms_list.exists():
            return SMS_VERIFICATION_FAILED

        if sms_list.count() > 1:
            # 如果有之前的验证码没有验证过
            # 则这些验证码统统过期
            for each in sms_list[1:]:
                each.status = SMS_OUT_OF_DATE
                each.save()

        sms_obj = sms_list[0]
        if sms_obj.is_out_of_date():
            sms_obj.status = SMS_OUT_OF_DATE
        else:
            if sms_obj.validate != validate:
                sms_obj.status = SMS_VERIFICATION_FAILED
            else:
                sms_obj.status = SMS_VERIFICATION_SUCCESS
        sms_obj.save()
        return sms_obj.status

    def __unicode__(self):
        return u'<phone: {}> <validate: {}> <status: {}>'.format(self.phone_number, self.validate, self.status)


class SMSValidateCheckFailures(models.Model):
    """
    This model will keep track of failed login attempts
    """

    MAX_FAILED_ATTEMPTS_ALLOWED = 3
    MAX_FAILED_ATTEMPTS_LOCKOUT_PERIOD_SECS = 30

    phone_number = models.CharField(blank=True, null=True, unique=True, max_length=50, db_index=True, default='')
    failure_count = models.IntegerField(default=0)
    lockout_until = models.DateTimeField(null=True)

    @classmethod
    def is_phone_locked_out(cls, phone_number):
        """
        Static method to return in a given phone_number has his/her account locked out
        """
        try:
            record = cls.objects.get(phone_number=phone_number)
            if record.failure_count < cls.MAX_FAILED_ATTEMPTS_ALLOWED:
                return False
        except cls.DoesNotExist:
            return False
        return True

    @classmethod
    def increment_lockout_counter(cls, phone_number):
        """
        Ticks the failed attempt counter
        """
        record, _ = cls.objects.get_or_create(phone_number=phone_number)
        record.failure_count = record.failure_count + 1
        max_failures_allowed = cls.MAX_FAILED_ATTEMPTS_ALLOWED

        # did we go over the limit in attempts
        if record.failure_count >= max_failures_allowed:
            # yes, then store when this account is locked out until
            lockout_period_secs = cls.MAX_FAILED_ATTEMPTS_LOCKOUT_PERIOD_SECS
            record.lockout_until = timezone.now() + timedelta(seconds=lockout_period_secs)
        record.save()

    @classmethod
    def clear_lockout_counter(cls, phone_number):
        """
        Removes the lockout counters (normally called after a successful register)
        """
        try:
            entry = cls.objects.get(phone_number=phone_number)
            entry.delete()
        except cls.DoesNotExist:
            return
