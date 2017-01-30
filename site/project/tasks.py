#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import time
import StringIO
import csv

from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.utils.translation import ugettext as _

# from celery import shared_task
from shareholder.models import Company
from project.celery import app
from utils.pdf import render_to_pdf
from utils.formatters import human_readable_segments


@app.task
def send_initial_password_mail(user, password):
    """
    task sending out email with new passwword via mandrill
    """

    msg = EmailMessage(
        subject=_('Welcome to Das Aktienregister - Your new password'),
        from_email="no-reply@das-aktienregister.ch",
        to=[user.email]
    )
    msg.template_name = "DARG_WELCOME_PASSWORD"
    msg.template_content = {}
    msg.global_merge_vars = {
        'NEW_PASSWORD': password,
    }
    msg.merge_vars = {}
    msg.send()


@app.task
def send_captable_pdf(user_id, company_id):
    user = User.objects.get(pk=user_id)
    company = Company.objects.get(pk=company_id)

    content = render_to_pdf(
        'active_shareholder_captable.pdf.html',
        {
            'pagesize': 'A4',
            'company': company,
            'today': datetime.datetime.now().date(),
            'total_capital': company.get_total_capital(),
            'currency': 'CHF',
            'provisioned_capital': company.get_provisioned_capital(),
            'securities_with_track_numbers': company.security_set.filter(
                track_numbers=True)
        }
    )

    filename = u'{}_captable_{}.pdf'.format(
        time.strftime("%Y-%m-%d"), company.name)

    msg = EmailMessage(
        subject=_('Your pdf captable file'),
        from_email="no-reply@das-aktienregister.ch",
        body=_('Your file is attached to this email'),
        to=[user.email]
    )
    msg.template_name = "DARG_FILE_DOWNLOAD"
    # msg.template_content = {}
    msg.global_merge_vars = {'FILE_DESC': _('PDF Captable/Active Shareholders')}
    # msg.merge_vars = {}
    msg.attach(filename, content, 'application/pdf')
    msg.send()


@app.task
def send_captable_csv(user_id, company_id):
    user = User.objects.get(pk=user_id)
    company = Company.objects.get(pk=company_id)
    track_numbers_secs = company.security_set.filter(track_numbers=True)
    filename = u'{}_captable_{}.csv'.format(
        time.strftime("%Y-%m-%d"), company.name)

    csvfile = StringIO.StringIO()
    writer = csv.writer(csvfile)
    # removed share percent due to heavy sql impact. killed perf for higher
    # shareholder count
    header = [
        _(u'shareholder number'), _(u'last name'), _(u'first name'),
        _(u'email'), _(u'share count'),  # _(u'votes share percent'),
        _(u'language ISO'), _('language full')]

    has_track_numbers = track_numbers_secs.exists()
    if has_track_numbers:
        header.append(_('Share IDs'))

    writer.writerow(header)

    # removed share percent due to heavy sql impact. killed perf for higher
    # shareholder count
    for shareholder in company.get_active_shareholders():
        row = [
            shareholder.number,
            shareholder.user.last_name,
            shareholder.user.first_name,
            shareholder.user.email,
            shareholder.share_count(),
            # shareholder.share_percent() or '--',
            shareholder.user.userprofile.language,
            shareholder.user.userprofile.get_language_display(),
        ]
        if has_track_numbers:
            text = ""
            for sec in track_numbers_secs:
                text += "{}: {} ".format(
                    sec.get_title_display(),
                    human_readable_segments(shareholder.current_segments(sec) or
                                            _('None'))
                )
            row.append(text)
        writer.writerow([unicode(s).encode("utf-8") for s in row])

    msg = EmailMessage(
        subject=_('Your csv captable file'),
        from_email="no-reply@das-aktienregister.ch",
        body=_('Your file is attached to this email'),
        to=[user.email]
    )
    msg.template_name = "DARG_FILE_DOWNLOAD"
    # msg.template_content = {}
    msg.global_merge_vars = {'FILE_DESC': _('CSV Captable/Active Shareholders')}
    # msg.merge_vars = {}
    msg.attach(filename, csvfile.getvalue(), 'text/csv')
    msg.send()
