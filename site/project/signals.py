#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib.auth.signals import user_logged_in
from django.core.mail import mail_admins


def notify_admin_on_signin(sender, request, user, **kwargs):
    subject = 'user {} signed in'.format(user.email)
    mail_admins(subject, subject)  # subject=message
    print 'sent admin notify'


user_logged_in.connect(notify_admin_on_signin)
