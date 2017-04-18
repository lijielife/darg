#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import datetime
import logging
import StringIO
import time

from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage
from django.utils import timezone
from django.utils.translation import ugettext as _
from natsort import natsorted

from project.celery import app
from reports.models import ORDERING_TYPES, REPORT_TYPES, Report
from shareholder.models import Company
from utils.formatters import human_readable_segments
from utils.pdf import render_to_pdf
from utils.http import url_with_domain

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
            if callable(getattr(unsorted_results[0], funcname)):
                return natsorted(
                    unsorted_results, key=lambda t:
                        unicode(getattr(t, funcname)() or 0), reverse=reverse)
            else:
                return natsorted(
                    unsorted_results, key=lambda t:
                        getattr(t, funcname), reverse=reverse)

        except TypeError:  # identify https://goo.gl/bDreXS
            logger.exception('ordering {} must be function of {} queryset '
                             'objects'.format(funcname, unsorted_results))
            raise

    # use conventional ordering
    return queryset.order_by(ordering)


def _add_file_to_report(filename, report, content):
    f = ContentFile(content)
    report.file.save(filename, f)
    report.save()


def _summarize_report(report):
    now = timezone.now()
    delta = now - report.created_at
    report.generation_time = delta.seconds
    report.generated_at = now
    report.save()


def _send_notify(user, filename, subject, body, file_desc, url=None):
    msg = EmailMessage(
        subject=subject,
        from_email="no-reply@das-aktienregister.ch",
        body=body,
        to=[user.email]
    )
    msg.template_name = "DARG_FILE_DOWNLOAD"
    msg.global_merge_vars = {'FILE_DESC': file_desc, 'URL': url}
    msg.send()


def _get_filename(report, company):
    return u'{}_{}_{}_{}.{}'.format(
        time.strftime("%Y-%m-%d"), report.report_type, report.order_by,
        company.name, report.file_type.lower())


def _prepare_report(company, report_type, ordering, file_type):
    """ create report object with predefined data """
    report = Report.objects.create(company=company, report_type=report_type,
                                   order_by=ordering, file_type=file_type,
                                   eta=timezone.now())
    report.update_eta()
    return report


@app.task
def render_captable_pdf(company_id, report_id, user_id=None, ordering=None,
                        notify=False, track_downloads=False):
    # prepare
    if user_id:
        user = User.objects.get(pk=user_id)
    company = Company.objects.get(pk=company_id)
    report = Report.objects.get(pk=report_id)
    ordering = _parse_ordering(ordering)
    filename = _get_filename(report, company)

    # render
    context = _get_captable_pdf_context(company, ordering)
    content = render_to_pdf(
        'active_shareholder_captable.pdf.html', context)

    # post process
    _add_file_to_report(filename, report, content)
    _summarize_report(report)

    if notify and user_id:
        _send_notify(user, filename, subject=_('Your pdf captable file'),
                     body=_('Your file is attached to this email'),
                     file_desc=_('PDF Captable/Active Shareholders'),
                     url=url_with_domain(report.get_absolute_url()))

    if not track_downloads:
        report.downloaded_at = datetime.datetime.now()
        report.save()


@app.task
def render_captable_csv(company_id, report_id, user_id=None, ordering=None,
                        notify=False, track_downloads=False):
    # prepare
    if user_id:
        user = User.objects.get(pk=user_id)
    company = Company.objects.get(pk=company_id)
    report = Report.objects.get(pk=report_id)
    ordering = _parse_ordering(ordering)
    filename = _get_filename(report, company)
    track_numbers_secs = company.security_set.filter(track_numbers=True)

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

    def to_unicode(iterable):
        return [unicode(s).encode("utf-8") for s in iterable]

    writer.writerow(to_unicode(header))

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
                                            [_('None')])
                )
            row.append(text)
        writer.writerow([unicode(s).encode("utf-8") for s in row])

    # post process
    csvfile.seek(0)
    _add_file_to_report(filename, report, csvfile.read())
    _summarize_report(report)

    if notify and user_id:
        _send_notify(user, filename, subject=_('Your csv captable file'),
                     body=_('Your file is attached to this email'),
                     file_desc=_('CSV Captable/Active Shareholders'),
                     url=url_with_domain(report.get_absolute_url()))

    if track_downloads:
        report.downloaded_at = datetime.datetime.now()
        report.save()


@app.task
def prerender_reports():
    """ prerender all reports each night for each company, each file type and
    each ordering for fast user access """

    for company in Company.objects.all():
        if company.shareholder_set.count() < 2:
            continue
        for (report_type, rname) in REPORT_TYPES:
            for (ordering, oname) in ORDERING_TYPES:
                # CSV
                report = _prepare_report(company, report_type, ordering, 'CSV')
                args = [company.pk, report.pk]
                kwargs = {'order_by': report.order_by}
                render_captable_csv.apply_async(args=args, kwargs=kwargs)

                # PDF
                report = _prepare_report(company, report_type, ordering, 'PDF')
                args = [company.pk, report.pk]
                kwargs = {'order_by': report.order_by}
                render_captable_pdf.apply_async(args=args, kwargs=kwargs)
