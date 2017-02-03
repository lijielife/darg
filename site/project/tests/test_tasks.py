#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core import mail
from django.test import TestCase

from project.generators import (UserGenerator,
                                ComplexShareholderConstellationGenerator)
from project.tasks import (send_initial_password_mail, _order_queryset,
                           _get_captable_pdf_context)
from shareholder.models import Shareholder


# --- TASKS
class TaskTestCase(TestCase):

    def setUp(self):
        self.shs, self.sec = ComplexShareholderConstellationGenerator().generate()

    def test_get_captable_pdf_context(self):

        res = _get_captable_pdf_context(self.shs[0].company,
                                        ordering='-share_count')
        self.assertEqual(len(res), 9)

    def test_order_queryset(self):

        qs = Shareholder.objects.all()

        ordering = '-user__first_name'
        res = _order_queryset(qs, ordering)
        self.assertEqual(list(res), list(qs.order_by(ordering)))

        ordering = 'share_count'
        res = _order_queryset(qs, ordering)
        self.assertEqual(res, sorted(qs, key=lambda t: t.share_count()))

    def test_send_initial_password_mail(self):

        password = 'SomePass'
        user = UserGenerator().generate()

        send_initial_password_mail(user, password)

        self.assertEqual(len(mail.outbox), 1)
