#!/usr/bin/python
# -*- coding: utf-8 -*-
import mock

from django.test import TestCase

from project.generators import ShareholderGenerator
from shareholder.models import Shareholder
from shareholder.signals import update_order_cache


class SignalTestCase(TestCase):

    @mock.patch('shareholder.signals.update_order_cache_task')
    def test_update_order_cache(self, task_mock):
        shareholder = ShareholderGenerator().generate()
        update_order_cache(Shareholder, shareholder, False)
        task_mock.apply_async.assert_called_with([shareholder.pk])
