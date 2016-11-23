#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib.auth.mixins import PermissionRequiredMixin


class OperatorPermissionRequiredMixin(PermissionRequiredMixin):

    def has_permission(self):
        """
        checks if logged in user has permission to access obj
        """
        if not self.request.user.is_authenticated():
            return False

        user = self.request.user
        obj = self.get_object()
        return obj.can_view(user)
