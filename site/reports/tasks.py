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


def _collect_csv_data(shareholder, security):
    # hide "None" strings
    def to_string_or_empty(value):
        if value and isinstance(value, list):
            # remove NoneTypes
            value = [v for v in value if v]
            value = u" , ".join(value)
        return unicode(value or u'')

    row = [
        shareholder.number,
        shareholder.user.userprofile.get_legal_type_display(),
        list(set([s.get_registration_type_display() for s
                  in shareholder.buyer.all()])),
        shareholder.user.userprofile.company_department,
        shareholder.user.userprofile.title,
        shareholder.user.userprofile.salutation,
        shareholder.user.last_name,
        shareholder.user.first_name,
        shareholder.user.userprofile.get_address(),
        shareholder.user.userprofile.postal_code,
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
        shareholder.share_count(security=security),
        shareholder.share_percent(security=security),
        shareholder.vote_percent(security=security),
        shareholder.cumulated_face_value(security=security),
        shareholder.is_management,
        shareholder.user.userprofile.language,
        shareholder.user.userprofile.get_language_display(),
    ]
    # remove any kind of empty data and replace by empty string. make all utf8
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
    return row


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
    # removed share percent due to heavy sql impact. killed perf for higher
    # shareholder count
    header = [
        _(u'shareholder number'), _('legal type'), _('registration types'),
        _('company_department'), _('title'), _('salutation'), _(u'last name'),
        _(u'first name'), _('address'), _('postal_code'), _('city'),
        _('birthday'), _('mailing_type'), _('nationality'), _('security type'),
        _('cusip'), _('face_value'), _('certificate_ids (issue date)'),
        _('stock book id'), _('depot_type'),
        _(u'email'), _(u'share count'),  _(u'share percent'),
        _('votes percent'),
        _('cumulated face value'), _('is management'),
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
        for security in company.security_set.all():
            if shareholder.share_count(security=security):
                row = _collect_csv_data(shareholder, security)
            else:
                continue

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
