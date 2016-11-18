#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse

from project.permissions import OperatorPermissionRequiredMixin
from project.generators import ShareholderGenerator
from shareholder.views import ShareholderView


class OperatorPermissionRequiredMixinTestCase(TestCase):
    """
    to be used as mixin for views which implement get_object method
    """
    def setUp(self):
        self.anon_user = AnonymousUser()
        self.factory = RequestFactory()
        self.shareholder = ShareholderGenerator().generate()

    def test_has_permission_anon_user(self):
        """
        test access fail on anon user
        """
        mixin = OperatorPermissionRequiredMixin()
        mixin.request = self.factory.get(
            reverse('shareholder', kwargs={'pk': self.shareholder.pk})
        )
        mixin.request.user = self.anon_user
        self.assertFalse(mixin.has_permission())

    def test_has_permission_authenticated_user(self):
        """
        test access fail on authenticated owner
        """
        view = ShareholderView()
        view.kwargs = {'pk': self.shareholder.pk}
        view.request = self.factory.get(
            reverse('shareholder', kwargs=view.kwargs)
        )
        view.request.user = self.shareholder.user
        self.assertTrue(view.has_permission())
