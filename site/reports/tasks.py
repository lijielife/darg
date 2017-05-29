#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
from decimal import Decimal
import datetime
import logging
import operator
import os
import StringIO
import sys
import time
from copy import deepcopy

from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.translation import ugettext as _
from natsort import natsorted

from project.celery import app
from reports.models import (ORDERING_TYPES, REPORT_FILE_TYPES, REPORT_TYPES,
                            Report)
from shareholder.models import Company
from utils.formatters import human_readable_segments
from utils.http import url_with_domain
from utils.pdf import render_to_pdf
from utils.xls import save_to_excel_file

logger = logging.getLogger(__name__)


# removed share percent due to heavy sql impact. killed perf for higher
# shareholder count
CSV_HEADER = [
    _(u'shareholder number'), _('legal type'), _('registration types'),
    _('company_department'), _('title'), _('salutation'), _(u'name'),
    _('address'), _('postal_code'), _('city'), _('country'),
    _('birthday'), _('mailing_type'), _('nationality'), _('security type'),
    _('cusip'), _('face_value'), _('certificate_ids (issue date)'),
    _('stock book id'), _('depot_type'),
    _(u'email'), _(u'share count'),  _(u'share percent'),
    _('votes percent'),
    _('cumulated face value'), _('is management'),
    _(u'language ISO'), _('language full')
]


def _get_captable_pdf_context(company, ordering, date):
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
            'ordering': ordering,
            'option_ordering': option_ordering,
            'report_date': date,
        }
    return context


def to_string_or_empty(value):
    if value and isinstance(value, list):
        # remove NoneTypes
        value = [v for v in value if v]
        value = u" , ".join(value)

    # casts
    if isinstance(value, (float, int, Decimal)):
        return value
    return unicode(value or u'')


def _collect_csv_data(shareholder, date):
    rows = []
    for security in shareholder.company.security_set.all():
        if shareholder.share_count(date=date, security=security):

            row = [
                shareholder.number,
                shareholder.user.userprofile.get_legal_type_display(),
                list(set([s.get_registration_type_display() for s
                          in shareholder.buyer.all()])),
                shareholder.user.userprofile.company_department,
                shareholder.user.userprofile.title,
                shareholder.user.userprofile.salutation,
                shareholder.get_full_name(),
                shareholder.user.userprofile.get_address(skip_city=True),
                shareholder.user.userprofile.postal_code,
                shareholder.user.userprofile.country,
                shareholder.user.userprofile.city,
                shareholder.user.userprofile.birthday,
                shareholder.get_mailing_type_display(),
                shareholder.user.userprofile.nationality,
                security,
                security.cusip,
                security.face_value,
                shareholder.get_certificate_ids(security=security),
                shareholder.get_stock_book_ids(security=security),
                shareholder.get_depot_types(security=security),
                shareholder.user.email,
                shareholder.share_count(security=security, date=date),
                float(shareholder.share_percent(security=security, date=date)),
                shareholder.vote_percent(security=security, date=date),
                shareholder.cumulated_face_value(security=security, date=date),
                shareholder.is_management,
                shareholder.user.userprofile.language,
                shareholder.user.userprofile.get_language_display(),
            ]
            # remove any kind of empty data and replace by empty string. make
            # all utf8
            row = [to_string_or_empty(val) for val in row]

            # handle track numbers
            if security.track_numbers:
                segments = human_readable_segments(
                    shareholder.current_segments(security)) or _('None')
                text = "{}: {} ".format(
                    security.get_title_display(),
                    segments
                )
                row.append(text)
            rows.append(row)
    return rows


def _collect_participation_csv_data(shareholder, date):
    row = [shareholder.number, shareholder.get_full_name(),
           shareholder.user.userprofile.get_address(skip_city=True),
           shareholder.user.userprofile.postal_code,
           shareholder.user.userprofile.city,
           shareholder.user.userprofile.country,
           shareholder.share_count(),
           shareholder.cumulated_face_value(),
           shareholder.vote_count()
           ]
    # remove any kind of empty data and replace by empty string. make
    # all utf8
    row = [to_string_or_empty(val) for val in row]

    return [row]


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

    # handle empyt QS
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
                _to_dotted(funcname)
                return natsorted(
                    unsorted_results, key=lambda t:
                        operator.attrgetter(funcname)(t), reverse=reverse)

        except TypeError:  # identify https://goo.gl/bDreXS
            logger.exception('ordering {} must be function of {} queryset '
                             'objects'.format(funcname, unsorted_results))
            raise

    # use conventional ordering
    return queryset.order_by(ordering)


def _add_file_to_report(filename, report, content=None):
    if content:
        f = ContentFile(content)
        report.file.save(filename, f)
    else:
        from django.core.files import File
        f = open(filename)
        report.file.save(filename, File(f))
    report.save()


def _summarize_report(report):
    now = timezone.now()
    delta = now - report.created_at
    report.generation_time = delta.seconds
    report.generated_at = now
    report.save()

    if report.generation_time > 3*60:
        logger.warning('report creation time took more then 3 mins: {}'.format(
            report.generation_time/60))


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


def _to_dotted(value):
    """ replaces `__` with `.` """
    return value.replace('__', '.')


def _get_filename(report, company):
    # xls special extension handling
    if report.file_type == 'XLS':
        return u'{}_{}_{}_{}.{}x'.format(
            time.strftime("%Y-%m-%d"), report.report_type, report.order_by,
            slugify(company.name), report.file_type.lower())

    return u'{}_{}_{}_{}.{}'.format(
        time.strftime("%Y-%m-%d"), report.report_type, report.order_by,
        slugify(company.name), report.file_type.lower())


def _prepare_report(company, report_type, ordering, file_type):
    """ create report object with predefined data """
    report = Report.objects.create(company=company, report_type=report_type,
                                   order_by=ordering, file_type=file_type,
                                   eta=timezone.now(), report_at=timezone.now())
    report.update_eta()
    return report


@app.task
def render_assembly_participation_xls(company_id, report_id, user_id=None,
                                      ordering=None, notify=False,
                                      track_downloads=False):
    # prepare
    if user_id:
        user = User.objects.get(pk=user_id)
    company = Company.objects.get(pk=company_id)
    report = Report.objects.get(pk=report_id)
    ordering = u'number'
    filename = _get_filename(report, company)

    header = [_('Shareholder#'), _('Full Name'), _('Address'),
              _('postal code'), _('city'), _('country'),
              _('share count'), _('capital'), _('vote count')]

    def to_unicode(iterable):
        return [unicode(s).encode("utf-8") for s in iterable]

    # for each active shareholder
    queryset = company.get_active_shareholders(date=report.report_at)
    queryset = _order_queryset(queryset, ordering)

    rows = []
    for shareholder in queryset:
        if shareholder.share_count(date=report.report_at):
            rows.extend(_collect_participation_csv_data(
                shareholder, report.report_at))
        else:
            continue

    # money_format
    formats = {'7': 'money_format'}
    save_to_excel_file(filename, rows, header, formats)

    # post process
    _add_file_to_report(filename, report)
    _summarize_report(report)

    if notify and user_id:
        _send_notify(user, filename,
                     subject=_('Your csv assembly participation file'),
                     body=_('Your file is attached to this email'),
                     file_desc=_('CSV Assembly Participation'),
                     url=url_with_domain(report.get_absolute_url()))

    if not track_downloads:
        report.downloaded_at = timezone.now()
        report.save()

    os.remove(filename)


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
    context = _get_captable_pdf_context(company, ordering,
                                        date=report.report_at)
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
        report.downloaded_at = timezone.now()
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

    header = deepcopy(CSV_HEADER)
    has_track_numbers = track_numbers_secs.exists()
    if has_track_numbers:
        header.append(_('Share IDs'))

    def to_unicode(iterable):
        return [unicode(s).encode("utf-8") for s in iterable]

    writer.writerow(to_unicode(header))

    # removed share percent due to heavy sql impact. killed perf for higher
    # shareholder count
    # for each active shareholder
    queryset = company.get_active_shareholders(date=report.report_at)
    queryset = _order_queryset(queryset, ordering)
    for shareholder in queryset:
        if shareholder.share_count(date=report.report_at):
            rows = _collect_csv_data(shareholder, report.report_at)
        else:
            continue

        for row in rows:
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

    if not track_downloads:
        report.downloaded_at = timezone.now()
        report.save()


@app.task
def render_captable_xls(company_id, report_id, user_id=None, ordering=None,
                        notify=False, track_downloads=False):
    # prepare
    if user_id:
        user = User.objects.get(pk=user_id)
    company = Company.objects.get(pk=company_id)
    report = Report.objects.get(pk=report_id)
    ordering = _parse_ordering(ordering)
    filename = _get_filename(report, company)
    track_numbers_secs = company.security_set.filter(track_numbers=True)

    header = deepcopy(CSV_HEADER)
    has_track_numbers = track_numbers_secs.exists()
    if has_track_numbers:
        header.append(_('Share IDs'))

    def to_unicode(iterable):
        return [unicode(s).encode("utf-8") for s in iterable]

    # removed share percent due to heavy sql impact. killed perf for higher
    # shareholder count
    # for each active shareholder
    queryset = company.get_active_shareholders(date=report.report_at)
    queryset = _order_queryset(queryset, ordering)
    rows = []
    for shareholder in queryset:
        if shareholder.share_count(date=report.report_at):
            rows.extend(_collect_csv_data(shareholder, report.report_at))
        else:
            continue

    # money_format
    formats = {'22': 'percent_format', '23': 'percent_format',
               '24': 'money_format'}
    save_to_excel_file(filename, rows, header, formats)

    # post process
    _add_file_to_report(filename, report)
    _summarize_report(report)

    if notify and user_id:
        _send_notify(user, filename, subject=_('Your xls captable file'),
                     body=_('Your file is attached to this email'),
                     file_desc=_('XLS Captable/Active Shareholders'),
                     url=url_with_domain(report.get_absolute_url()))

    if not track_downloads:
        report.downloaded_at = timezone.now()
        report.save()

    os.remove(filename)  # del tmp file


@app.task
def prerender_reports():
    """ prerender all reports each night for each company, each file type and
    each ordering for fast user access """

    for company in Company.objects.all():
        if company.shareholder_set.count() < 2:
            continue
        for (report_type, rname) in REPORT_TYPES:
            for file_type, fname in REPORT_FILE_TYPES:
                for (ordering, oname) in ORDERING_TYPES:
                    if report_type == 'assembly_participation' and (
                            ordering != 'number' or file_type != 'XLS'):
                        continue
                    report = _prepare_report(
                        company, report_type, ordering, fname)
                    args = [company.pk, report.pk]
                    kwargs = {'ordering': report.order_by}
                    method_name = 'render_{}_{}'.format(report_type.lower(),
                                                        fname.lower())
                    method = getattr(sys.modules[__name__], method_name)
                    method.apply_async(args=args, kwargs=kwargs)
