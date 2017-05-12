#!/usr/bin/python
# -*- coding: utf-8 -*-
import mock
from django.test import TestCase
from model_mommy import mommy

from project.generators import ShareholderGenerator
from shareholder.models import Position, Shareholder
from shareholder.signals import update_order_cache


class SignalTestCase(TestCase):

    @mock.patch('shareholder.signals.update_order_cache_task')
    def test_update_order_cache(self, task_mock):
        shareholder = ShareholderGenerator().generate()
        update_order_cache(Shareholder, shareholder, False)
        task_mock.apply_async.assert_called_with([shareholder.pk])

        task_mock.reset_mock()
        position = mommy.make(Position, _fill_optional=True)
        update_order_cache(Position, position, False)
        calls = (mock.call(position.buyer.pk), mock.call(position.seller.pk))
        task_mock.apply_async.has_calls(calls)
