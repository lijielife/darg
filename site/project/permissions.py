#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib.auth.mixins import PermissionRequiredMixin


class OperatorPermissionRequiredMixin(PermissionRequiredMixin):

    def has_permission(self):
        """
        checks if logged in user has permission to access obj
        """
        user = self.request.user
        obj = self.get_object()
        return obj.can_view(user)
