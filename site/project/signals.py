#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime

from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.core.mail import mail_admins


def notify_admin_on_signin(sender, request, user, **kwargs):
    if not settings.DEBUG:
        subject = 'user {} signed in'.format(user.email)
        mail_admins(subject, subject)  # subject=message
        print 'sent admin notify'


def set_company_in_session(sender, user, request, **kwargs):
    """
    for multi company users, we need to setup at least one default
    company inside the session, so we have a default company to show
    """
    operator = user.operator_set.order_by(
        '-last_active_at').first()

    # None if regular shareholder
    if operator:
        request.session['company_pk'] = operator.company.pk
        operator.last_active_at = datetime.datetime.now()


user_logged_in.connect(set_company_in_session)
user_logged_in.connect(notify_admin_on_signin)
