#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import time
import StringIO
import csv
import logging

from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.utils.translation import ugettext as _

# from celery import shared_task
from shareholder.models import Company
from project.celery import app
from utils.pdf import render_to_pdf
from utils.formatters import human_readable_segments

logger = logging.getLogger(__name__)


def _get_captable_pdf_context(company, ordering):
    """
    isolated code to make for better testing
    """
    option_ordering = ordering.replace('share', 'options')
    context = {
            'pagesize': 'A4',
            'company': company,
            'today': datetime.datetime.now().date(),
            'total_capital': company.get_total_capital(),
            'currency': 'CHF',
            'provisioned_capital': company.get_provisioned_capital(),
            'securities_with_track_numbers': company.security_set.filter(
                track_numbers=True),
            'active_shareholders': _order_queryset(
                company.get_active_shareholders(), ordering),
            'active_option_holders': _order_queryset(
                company.get_active_option_holders(), option_ordering),
        }
    return context


def _parse_ordering(ordering):
    """
    parse ordering from js:
    name -> 'name'
    name_desc -> '-name'
    """
    if not ordering:
        return 'user__last_name'
    if ordering.endswith('_desc'):
        return u'-' + ordering[:-5]
    else:
        return ordering


def _order_queryset(queryset, ordering):
    """
    if the ordering is a field name, order by this one. otherwise check if the
    ordering is a function and then evaluate the QS and order by function
    """
    reverse = False
    funcname = ordering
    if ordering.startswith('-'):
        funcname = ordering[1:]
        reverse = True

    # handle empyyt QS
    if not queryset:
        return queryset.model.objects.none()

    # handle sort by function result
    if hasattr(queryset.first(), funcname):
        unsorted_results = queryset.all()
        try:
            return sorted(
                unsorted_results, key=lambda t: float(getattr(t, funcname)()),
                reverse=reverse)
        except TypeError:  # identify https://goo.gl/bDreXS
            logger.exception('ordering {} must be function of {} queryset '
                             'objects'.format(funcname, unsorted_results))

    # use conventional ordering
    return queryset.order_by(ordering)


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
def send_captable_pdf(user_id, company_id, ordering=None):
    user = User.objects.get(pk=user_id)
    company = Company.objects.get(pk=company_id)
    ordering = _parse_ordering(ordering)
    context = _get_captable_pdf_context(company, ordering)
    content = render_to_pdf(
        'active_shareholder_captable.pdf.html',
        context,
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
def send_captable_csv(user_id, company_id, ordering=None):
    user = User.objects.get(pk=user_id)
    company = Company.objects.get(pk=company_id)
    track_numbers_secs = company.security_set.filter(track_numbers=True)
    filename = u'{}_captable_{}.csv'.format(
        time.strftime("%Y-%m-%d"), company.name)
    ordering = _parse_ordering(ordering)

    csvfile = StringIO.StringIO()
    writer = csv.writer(csvfile)
    # removed share percent due to heavy sql impact. killed perf for higher
    # shareholder count
    header = [
        _(u'shareholder number'), _(u'last name'), _(u'first name'),
        _(u'email'), _(u'share count'),  _(u'votes share percent'),
        _(u'language ISO'), _('language full')]

    has_track_numbers = track_numbers_secs.exists()
    if has_track_numbers:
        header.append(_('Share IDs'))

    writer.writerow(header)

    # removed share percent due to heavy sql impact. killed perf for higher
    # shareholder count
    queryset = company.get_active_shareholders()
    queryset = _order_queryset(queryset, ordering)
    for shareholder in queryset:
        row = [
            shareholder.number,
            shareholder.user.last_name,
            shareholder.user.first_name,
            shareholder.user.email,
            shareholder.share_count(),
            shareholder.share_percent() or '--',
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
