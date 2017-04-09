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
        self.shs, self.sec = (
            ComplexShareholderConstellationGenerator().generate())

    def test_get_captable_pdf_context(self):

        res = _get_captable_pdf_context(self.shs[0].company,
                                        ordering='-share_count')
        self.assertEqual(len(res), 9)

        # order by share percent
        res = _get_captable_pdf_context(self.shs[0].company,
                                        ordering='-share_percent')
        self.assertEqual(len(res), 9)
        for idx, sh in enumerate(res['active_shareholders']):
            if idx == 0:
                continue
            self.assertLessEqual(
                float(sh.share_percent()),
                float(res['active_shareholders'][idx-1].share_percent()))

        # order by share_count
        res = _get_captable_pdf_context(self.shs[0].company,
                                        ordering='-share_count')
        self.assertEqual(len(res), 9)
        for idx, sh in enumerate(res['active_shareholders']):
            if idx == 0:
                continue
            self.assertLessEqual(
                int(sh.share_count(security=self.sec)),
                int(res['active_shareholders'][idx-1].share_count(
                    security=self.sec)))

        # order by number
        res = _get_captable_pdf_context(self.shs[0].company,
                                        ordering='-number')
        self.assertEqual(len(res), 9)
        for idx, sh in enumerate(res['active_shareholders']):
            if idx == 0:
                continue
            self.assertLessEqual(
                sh.number,
                res['active_shareholders'][idx-1].number)

        # order by number
        res = _get_captable_pdf_context(self.shs[0].company,
                                        ordering='-user__last_name')
        self.assertEqual(len(res), 9)
        for idx, sh in enumerate(res['active_shareholders']):
            if idx == 0:
                continue
            self.assertLessEqual(
                sh.user.last_name,
                res['active_shareholders'][idx-1].user.last_name.lower())

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
