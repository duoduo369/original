# -*- coding: utf-8 -*-
import logging
from rest_framework.permissions import BasePermission

logger = logging.getLogger(__name__)


class IsCMSAuthenticated(BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if request.user.is_cms_user:
                return True
            logger.info('request cms api, but not cms_user: %s', request.user.id)
        return False
