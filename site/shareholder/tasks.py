#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os
import logging

import requests
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import (EmailMessage, EmailMultiAlternatives,
                              mail_admins, send_mail)
from django.core.urlresolvers import reverse
from django.template import Context, loader
from django.utils.formats import date_format
from django.utils.text import slugify
from django.utils.timezone import datetime, now, timedelta
from django.utils.translation import activate as activate_lang
from django.utils.translation import ugettext as _
from django.utils import timezone

from pingen.api import Pingen
from project.celery import app
from shareholder.import_backends import SwissBankImportBackend
from utils.pdf import render_pdf

from .models import Company, ShareholderStatement, ShareholderStatementReport

logger = logging.getLogger(__name__)


# helpers
# FIXME: maybe move this to shareholder/utils.py or utils/

def _context_email_defaults():
    version = getattr(settings, 'VERSION', False)
    return dict(
        domain=Site.objects.get_current().domain,
        VERSION=version and 'v{}'.format(version) or ''
    )


@app.task
def send_statement_generation_operator_notify():
    """
    send a notification to company operators that shareholder statements will
    be generated and sent in
    `settings.SHAREHOLDER_STATEMENT_OPERATOR_NOTIFY_DAYS` days
    """
    offset = getattr(settings, 'SHAREHOLDER_STATEMENT_OPERATOR_NOTIFY_DAYS', 7)
    scheduled = now().date() + timedelta(days=offset)
    queryset = Company.objects.filter(is_statement_sending_enabled=True,
                                      statement_sending_date=scheduled)

    activate_lang(settings.LANGUAGE_CODE)

    for company in queryset:

        # check subscription
        if not company.has_feature_enabled('shareholder_statements'):
            continue

        operators = [op.user.email for op in company.get_operators()
                     if op.user.is_active and op.user.email]

        if not operators:
            mail_admins(
                _('Company has not operators'),
                _('Company {} (ID: {}) has no active operator(s) with an '
                  'email address!').format(company.name, company.pk)
            )
            continue

        context = dict(
            company_name=company.name,
            report_date=date_format(company.statement_sending_date),
            company_url='{}://{}{}'.format(
                (getattr(settings, 'FORCE_SECURE_CONNECTION',
                         not settings.DEBUG) and 'https' or 'http'),
                Site.objects.get_current().domain,
                reverse('company', args=[company.pk])
            )
        )

        if ('djrill' in settings.EMAIL_BACKEND and
                getattr(
                    settings,
                    'MANDRILL_SHAREHOLDER_STATEMENT_OPERATOR_NOTIFY_TEMPLATE',
                    None)):
            # use mandrill template
            template_name = getattr(
                settings,
                'MANDRILL_SHAREHOLDER_STATEMENT_OPERATOR_NOTIFY_TEMPLATE'
            )
            msg = EmailMessage()
            # mandrill settings
            msg.template_name = template_name
            msg.use_template_subject = True  # use template subject
            msg.use_template_from = False  # FIXME: use our setting?
            msg.global_merge_vars = context
        else:
            # use default/fallback
            msg = EmailMultiAlternatives()
            msg.subject = _(
                'Shareholder statement about to be sent for {company}').format(
                    **dict(company=company.name))
            # text body
            context.update(**_context_email_defaults())
            msg.body = loader.render_to_string(
                'email/statement_operator_notify.txt', context,
                Context(autoescape=False))
            # html alternative
            html_body = loader.render_to_string(
                'email/statement_operator_notify.html', context)
            msg.attach_alternative(html_body, 'text/html')

        msg.to = operators

        # add statement preview
        preview_context = dict(
            user_name=_('Preview'),
            company=company,
            report_date=now().date(),
            site=Site.objects.get_current(),
            STATIC_URL=settings.STATIC_URL,
            preview=True
        )
        preview_html = loader.render_to_string(
            company.statement_template.template.name, preview_context)
        try:
            preview_pdf = render_pdf(preview_html)
        except:
            preview_pdf = None

        if preview_pdf:
            preview_file_name = u'{}-statement-preview.pdf'.format(
                slugify(company.name))
            msg.attach(
                preview_file_name,
                preview_pdf,
                'application/pdf'
            )
        else:
            # TODO: what now?
            pass

        result = msg.send()

        if not result:
            mail_admins(
                _('Shareholder Statement Operator Notify failed'),
                _('The notification for company operators about an upcoming '
                  'statement generation could not be sent:\n\n{}\n\n'
                  'The company is: {} (ID: {})').format(
                    (getattr(result, 'mandrill_response', None) and
                        result.mandrill_response[0] or _('[No information]')),
                    company.name, company.pk
                )
            )


@app.task
def send_statement_report_operator_notify():
    """
    send a notification to company operators that a report for shareholder
    statements is available
    `settings.SHAREHOLDER_STATEMENT_REPORT_OPERATOR_NOTIFY_DAYS` days
    """
    offset = getattr(
        settings, 'SHAREHOLDER_STATEMENT_REPORT_OPERATOR_NOTIFY_DAYS', 14)
    scheduled = now().date() - timedelta(days=offset)
    queryset = ShareholderStatementReport.objects.filter(report_date=scheduled)

    activate_lang(settings.LANGUAGE_CODE)

    for report in queryset:
        operators = [op.user.email for op in report.company.get_operators()
                     if op.user.is_active and op.user.email]

        if not operators:
            mail_admins(
                _('Company has not operators'),
                _('Company {} (ID: {}) has no active operator(s) with an '
                  'email address!').format(report.company.name,
                                           report.company.pk)
            )
            continue

        # users that would've received letter but have no address
        no_letter_statements = report.shareholderstatement_set.filter(
            pdf_downloaded_at=None, letter_sent_at=None)
        users_without_address = [s.user for s in no_letter_statements
                                 if not s.user.userprofile.has_address]

        context = dict(
            company_name=report.company.name,
            report_date=date_format(report.report_date),
            statement_count=report.statement_count,
            statement_sent_count=report.statement_sent_count,
            statement_opened_count=report.statement_opened_count,
            statement_downloaded_count=report.statement_downloaded_count,
            statement_letter_count=report.statement_letter_count,
            users_without_address=[
                {'id': user.pk, 'name': user.get_full_name() or user.email}
                for user in users_without_address
            ],
            report_url='{}://{}{}'.format(
                (getattr(settings, 'FORCE_SECURE_CONNECTION',
                         not settings.DEBUG) and 'https' or 'http'),
                Site.objects.get_current().domain,
                reverse('statement_report', args=[report.pk])
            )
        )

        if ('djrill' in settings.EMAIL_BACKEND and
                getattr(
                    settings,
                    ('MANDRILL_SHAREHOLDER_STATEMENT_REPORT_'
                     'OPERATOR_NOTIFY_TEMPLATE'),
                    None)):
            # use mandrill template
            template_name = getattr(
                settings,
                ('MANDRILL_SHAREHOLDER_STATEMENT_REPORT_'
                 'OPERATOR_NOTIFY_TEMPLATE')
            )
            msg = EmailMessage()
            # mandrill settings
            msg.template_name = template_name
            msg.use_template_subject = True  # use template subject
            msg.use_template_from = False  # FIXME: use our setting?
            msg.global_merge_vars = context
        else:
            # use default/fallback
            msg = EmailMultiAlternatives()
            msg.subject = _(
                'Shareholder statement report for {company}').format(
                    **dict(company=report.company.name))
            # text body
            context.update(**_context_email_defaults())
            msg.body = loader.render_to_string(
                'email/statement_report_operator_notify.txt', context,
                Context(autoescape=False))
            # html alternative
            html_body = loader.render_to_string(
                'email/statement_report_operator_notify.html', context)
            msg.attach_alternative(html_body, 'text/html')

        msg.to = operators
        result = msg.send()

        if not result:
            mail_admins(
                _('Shareholder Statement Report Operator Notify failed'),
                _('The notification for company operators about a report for '
                  'shareholder statements could not be sent:\n\n{}\n\n'
                  'The company is: {} (ID: {})').format(
                    (getattr(result, 'mandrill_response', None) and
                        result.mandrill_response[0] or _('[No information]')),
                    report.company.name, report.company.pk
                )
            )


@app.task
def generate_statements_report():
    """
    generate shareholder statement report and statements for companies with
    statement sending date set to today
    """
    today = now().date()
    company_qs = Company.objects.filter(is_statement_sending_enabled=True,
                                        statement_sending_date=today)
    for company in company_qs:

        # check subscription
        if not company.has_feature_enabled('shareholder_statements'):
            continue

        report, created = company.shareholderstatementreport_set.get_or_create(
            report_date=today)

        # FIXME: should we do anything, if report not created here?

        report.generate_statements()


@app.task
def send_statement_email(statement_id):
    """
    send email to user with shareholder statement
    """

    qs = ShareholderStatement.objects.filter(pk=statement_id)

    if not qs.exists():
        # TODO: error handling?!
        return 0

    obj = qs.get()

    activate_lang(settings.LANGUAGE_CODE)

    # check necessarities first

    if not obj.user.email:
        # mail operators
        operators = [op.user.email for op in obj.report.company.get_operators()
                     if op.user.is_active and op.user.email]
        send_mail(
            _('A user is missing an email address'),
            _('The following users, who is a shareholder of {company} '
              'is missing an email address.\n\n{user} (ID: {user_id})\n\n'
              'We can not send him the shareholder statement until a valid'
              ' email address is provided.').format(**dict(
                  user=obj.user.get_full_name() or obj.user.username,
                  user_id=obj.user_id,
                  company=obj.report.company.name
              )),
            settings.DEFAULT_FROM_EMAIL,
            operators)
        return 0  # we play along with django email api

    elif not obj.pdf_file or not os.path.isfile(obj.pdf_file):
        # mail operators
        operators = [op.user.email for op in obj.report.company.get_operators()
                     if op.user.is_active and op.user.email]
        send_mail(
            _('A statement is missing the PDF file'),
            _('The following statement of user {user} is missing '
              'the PDF file.\n\n{statement} (ID: {statement_id})\n\n'
              'We can not send him the shareholder statement until a valid'
              ' file is provided.').format(**dict(
                  user=obj.user.get_full_name() or obj.user.username,
                  statement=obj,
                  statement_id=obj.pk
              )),
            settings.DEFAULT_FROM_EMAIL,
            operators)
        return 0  # we play along with django email api

    # ok, we should be fine to send the email with the PDF link

    shareholders = obj.user.shareholder_set.filter(
        company_id=obj.report.company_id)
    letter_sent_offset = getattr(
        settings, 'SHAREHOLDER_STATMENT_LETTER_OFFSET_DAYS', 7)
    context = dict(
        user_name=obj.user.get_full_name() or obj.user.email,
        company_name=obj.report.company.name,
        shareholder_numbers=shareholders.values_list('number', flat=True),
        report_date=date_format(obj.report.report_date),
        download_url=obj.get_pdf_download_url(with_auth_token=True),
        letter_sent_offset=letter_sent_offset,
        user_has_address=obj.user.userprofile.has_address
    )

    if ('djrill' in settings.EMAIL_BACKEND and
            getattr(settings, 'MANDRILL_SHAREHOLDER_STATEMENT_TEMPLATE',
                    None)):
        # use mandrill template
        template_name = settings.MANDRILL_SHAREHOLDER_STATEMENT_TEMPLATE
        msg = EmailMessage()
        # mandrill settings
        msg.template_name = template_name
        msg.use_template_subject = True  # use template subject
        msg.use_template_from = False  # FIXME: use our setting?
        msg.track_opens = True  # regardless of global setting
        msg.global_merge_vars = context
    else:
        # use default/fallback
        msg = EmailMultiAlternatives()
        msg.subject = _(
            'Your personal shareholder statement for {company}').format(
                **dict(company=obj.report.company))
        # text body
        context.update(**_context_email_defaults())
        msg.body = loader.render_to_string('email/statement.txt', context,
                                           Context(autoescape=False))
        # html alternative
        html_body = loader.render_to_string('email/statement.html', context)
        msg.attach_alternative(html_body, 'text/html')

    msg.to = [obj.user.email]

    result = msg.send()

    if result:
        if getattr(msg, 'mandrill_response', None):
            response = msg.mandrill_response[0]
            sep = getattr(settings, 'REMOTE_EMAIL_SEPARATOR', '$')
            obj.remote_email_id = 'mandrill{}{}'.format(
                sep, response['_id'])

        obj.email_sent_at = now()
        obj.save()

    return result


@app.task
def fetch_statement_email_opened_mandrill():
    """
    try to fetch the "opened at" tracking via mandrill
    """

    api_url = settings.MANDRILL_API_BASE_URL + 'messages/info.json'
    sep = getattr(settings, 'REMOTE_EMAIL_SEPARATOR', '$')

    offset = getattr(settings, 'SHAREHOLDER_STATEMENT_EMAIL_OPENED_DAYS', 7)
    statement_qs = ShareholderStatement.objects.filter(
        email_opened_at=None,
        email_sent_at__gte=now() - timedelta(days=offset),
        remote_email_id__startswith='mandrill{}'.format(sep)
    )

    for statement in statement_qs:
        provider, remote_id = statement.remote_email_id.split(sep, 1)
        data = dict(key=settings.MANDRILL_API_KEY, id=remote_id)
        response = requests.get(api_url, data=json.dumps(data))
        if response.status_code == 200:
            # check if opened timestamp in response
            response_data = response.json()
            if response_data.get('state') == 'sent':
                opens_detail = response_data.get('opens_detail', [])
                if not opens_detail:
                    # found no timestamp
                    continue
                ts = opens_detail[0].get('ts')
                if isinstance(ts, int):
                    # found a timestamp ... set value on instance
                    statement.email_opened_at = timezone.make_aware(
                        datetime.fromtimestamp(ts))
                    statement.save()
        else:
            logger.warning('bad mandrill response on email open fetching',
                           extra={'response': response.content})


@app.task
def send_statement_letter(statement_id):
    """
    send letter to statement user via service
    """
    qs = ShareholderStatement.objects.filter(
        pk=statement_id,
        report__company__send_shareholder_statement_via_letter_enabled=True)

    if not qs.exists():
        # TODO: error handling?!
        return False

    obj = qs.get()

    if not obj.user.userprofile.has_address:
        # bummer
        return False

    # call service to send obj.pdf_file as letter to obj.user
    api = Pingen()
    result = api.upload_document(obj.pdf_file)
    if result:
        obj.letter_sent_at = now()
        obj.save()


@app.task
def send_statement_letters():
    """
    send letter statements to all shareholder users, that did not downloaded
    the pdf file (in time)
    """
    offset = getattr(settings, 'SHAREHOLDER_STATMENT_LETTER_OFFSET_DAYS', 7)
    report_date = now().date() - timedelta(days=offset)
    # find reports
    report_qs = ShareholderStatementReport.objects.filter(
        report_date=report_date)
    for report in report_qs:
        # find statements that were not downloaded (in time)
        statement_qs = report.shareholderstatement_set.filter(
            pdf_downloaded_at=None, letter_sent_at=None)
        for statement in statement_qs:
            # check if statement user has an postal address
            if not statement.user.userprofile.has_address:
                # bummer
                logger.warning('cannot send statement, missing address',
                               extra={'statement_pk': statement.pk})
                continue

            # send letter via service to user
            send_statement_letter.delay(statement.pk)


@app.task
def update_banks_from_six():
    """
    regularly update swiss banks database with data from six
    """
    SwissBankImportBackend().update()
