#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core import mail
from django.test import TestCase

from project.generators import UserGenerator
from project.tasks import send_initial_password_mail


# --- TASKS
class TaskTestCase(TestCase):

    def test_send_initial_password_mail(self):

        password = 'SomePass'
        user = UserGenerator().generate()

        send_initial_password_mail(user, password)

        self.assertEqual(len(mail.outbox), 1)
