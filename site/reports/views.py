import time

import dateutil.parser
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView
from sendfile import sendfile

from reports.models import Report
from reports.tasks import to_string_or_empty
from shareholder.models import (Company, Operator, OptionTransaction, Position,
                                Security)
from utils.session import get_company_from_request
from utils.xls import save_to_excel_file

XLSX_CONTENT_TYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'


def _get_contacts(company):

    rows = []
    for shareholder in company.get_active_shareholders():
        row = [
            shareholder.number,
            shareholder.user.last_name,
            shareholder.user.first_name,
            shareholder.user.email,
            shareholder.user.userprofile.language,
            shareholder.user.userprofile.get_language_display(),
            shareholder.user.userprofile.street,
            shareholder.user.userprofile.street2,
            shareholder.user.userprofile.c_o,
            shareholder.user.userprofile.city,
            shareholder.user.userprofile.postal_code,
            (shareholder.user.userprofile.country.name
                if shareholder.user.userprofile.country else u''),
            shareholder.user.userprofile.pobox,
            shareholder.get_mailing_type_display(),
            (shareholder.user.userprofile.nationality.name
                if shareholder.user.userprofile.nationality else u'')
        ]
        rows.append(row)

    for shareholder in company.get_active_option_holders():
        row = [
            shareholder.number,
            shareholder.user.last_name,
            shareholder.user.first_name,
            shareholder.user.email,
            shareholder.user.userprofile.language,
            shareholder.user.userprofile.get_language_display(),
            shareholder.user.userprofile.street,
            shareholder.user.userprofile.street2,
            shareholder.user.userprofile.c_o,
            shareholder.user.userprofile.city,
            shareholder.user.userprofile.postal_code,
            (shareholder.user.userprofile.country.name
                if shareholder.user.userprofile.country else u''),
            shareholder.user.userprofile.pobox,
            shareholder.get_mailing_type_display(),
            (shareholder.user.userprofile.nationality.name
                if shareholder.user.userprofile.nationality else u'')
        ]
        rows.append(row)

    return rows


def _get_transactions(from_date, to_date, security, company):
    rows = []

    for position in Position.objects.filter(
        bought_at__range=(from_date, to_date), security=security
    ).filter(
        Q(buyer__company=company) | Q(seller__company=company)
    ).prefetch_related('buyer', 'seller', 'security'):
        row = [
            position.bought_at,
            position.buyer.get_full_name() if position.buyer else u"",
            position.seller.get_full_name() if position.seller else u"",
            position.count,
            position.value,
            unicode(position.security),
            position.comment,
            position.get_depot_type_display(),
            position.stock_book_id
        ]
        rows.append(row)

    rows.append([_('----------------------------------------')])
    rows.append([_('Transactions for options:')])
    rows.append([_('----------------------------------------')])

    for optiontransaction in OptionTransaction.objects.filter(
        bought_at__range=(from_date, to_date), option_plan__security=security
    ).filter(
        Q(buyer__company=company) | Q(seller__company=company)
    ).prefetch_related(
        'buyer', 'seller', 'option_plan', 'option_plan__security'
    ):
        row = [
            optiontransaction.bought_at,
            optiontransaction.buyer.get_full_name(),
            optiontransaction.seller.get_full_name(),
            optiontransaction.count,
            optiontransaction.option_plan.exercise_price,
            unicode(optiontransaction.option_plan.security),
            '',
            optiontransaction.get_depot_type_display(),
            optiontransaction.stock_book_id,
            optiontransaction.vesting_months,
            optiontransaction.certificate_id,
        ]
        rows.append(row)

    return rows


@login_required
def report_download(request, report_id):
    """ check for user is operator and send download of report file """
    report = get_object_or_404(Report, id=report_id)
    if report.company.operator_set.filter(user=request.user).exists():
        if not report.downloaded_at:
            report.downloaded_at = timezone.now()
            report.save()
        return sendfile(request, report.file.path, attachment=True,
                        attachment_filename=report.get_filename())
    else:
        return HttpResponseForbidden(_("Permission denied"))


@login_required
def contacts_xls(request, company_id):
    """ returns xls with active shareholders """

    # perm check
    if not Operator.objects.filter(
        user=request.user, company__id=company_id
    ).exists():
        return HttpResponseForbidden()

    company = get_object_or_404(Company, id=company_id)

    # Create the HttpResponse object with the appropriate content header.
    filename = "{}_contacts_{}.xlsx".format(time.strftime("%Y-%m-%d"),
                                            slugify(company.name))
    response = HttpResponse(
        content_type=XLSX_CONTENT_TYPE)
    response['Content-Disposition'] = (
        u'attachment; filename="{}"'.format(filename))

    _rows = _get_contacts(company)
    header = [
        _(u'shareholder number'), _(u'last name'), _(u'first name'),
        _(u'email'),
        _(u'language ISO'), _('language full'), _('street'), _('street 2'),
        _('c/o'), _('city'), _('zip'), _('country'),
        _('pobox'), _('mailing type'), _('nationality'),
    ]

    rows = []
    for row in _rows:
        rows.append([to_string_or_empty(s) for s in row])

    save_to_excel_file(filename, rows, header, response=response)
    return response


@login_required
def transactions_xls(request, company_id):
    """ returns xls with transactions """

    # perm check
    if not Operator.objects.filter(
        user=request.user, company__id=company_id
    ).exists():
        return HttpResponseForbidden()

    company = get_object_or_404(Company, id=company_id)
    security = get_object_or_404(Security, id=request.GET.get('security'))
    from_date = dateutil.parser.parse(request.GET.get('from'))
    to_date = dateutil.parser.parse(request.GET.get('to'))

    # Create the HttpResponse object with the appropriate XLS header.
    filename = "{}_transactions_{}_.xlsx".format(
        time.strftime("%Y-%m-%d"), slugify(company.name),
        slugify(security.get_title_display()))
    response = HttpResponse(content_type=XLSX_CONTENT_TYPE)
    response['Content-Disposition'] = (
        u'attachment; filename="{}"'.format(filename))

    header = [
        _(u'date'), _(u'buyer'), _(u'seller'),
        _(u'count'),
        _(u'value'), _('security'), _('comment'), _('depot type'),
        _('stock book id'), _(u'vesting period (options only'),
        _(u'cert id (options only)'),
    ]

    _rows = _get_transactions(from_date, to_date, security, company)
    rows = []
    for row in _rows:
        rows.append([to_string_or_empty(s) for s in row])

    save_to_excel_file(filename, rows, header, response=response)

    return response


@login_required
def printed_certificates_xls(request, company_id):
    """
    return xls with list of printed certificates
    """
    # perm check
    if not Operator.objects.filter(
        user=request.user, company__id=company_id
    ).exists():
        return HttpResponseForbidden()

    company = get_object_or_404(Company, id=company_id)

    # Create the HttpResponse object with the appropriate content header.
    filename = "{}_printed_certificates_{}.xlsx".format(
        time.strftime("%Y-%m-%d"), slugify(company.name))
    response = HttpResponse(content_type=XLSX_CONTENT_TYPE)
    response['Content-Disposition'] = (
        u'attachment; filename="{}"'.format(filename))

    ots = OptionTransaction.objects.filter(
        option_plan__company=company,
        printed_at__isnull=False,
        certificate_id__isnull=False,
        ).distinct()
    pos = Position.objects.filter(
        Q(buyer__company=company) | Q(seller__company=company),
        printed_at__isnull=False,
        certificate_id__isnull=False,
        ).distinct()
    header = [_('full name'), _('share count'), _('security name'),
              _('certificate id'), _('certificate printed at'),
              _('security type')]
    # add option transactions
    _rows = []
    _rows += [
        [ot.buyer.get_full_name(),
         ot.count,
         unicode(ot.option_plan.security),
         ot.certificate_id,
         ot.printed_at, _('option')]
        for ot in ots]
    # add positions
    _rows += [
        [ot.buyer.get_full_name(),
         ot.count,
         unicode(ot.security),
         ot.certificate_id,
         ot.printed_at, _('stock')]
        for ot in pos]
    # render xls
    rows = []
    for row in _rows:
        rows.append([to_string_or_empty(s) for s in row])

    save_to_excel_file(filename, rows, header, response=response)

    return response


@login_required
def vested_xls(request, company_id):
    """
    return xls with list of vested shareholders and positions
    """
    # perm check
    if not Operator.objects.filter(
        user=request.user, company__id=company_id
    ).exists():
        return HttpResponseForbidden()

    company = get_object_or_404(Company, id=company_id)

    # Create the HttpResponse object with the appropriate content header.
    filename = "{}_vested_{}.xlsx".format(
        time.strftime("%Y-%m-%d"), slugify(company.name))
    response = HttpResponse(content_type=XLSX_CONTENT_TYPE)
    response['Content-Disposition'] = (
        u'attachment; '
        u'filename="{}"'.format(filename))

    positions = Position.objects.filter(
        Q(buyer__company=company) | Q(seller__company=company),
        vesting_months__gt=0).distinct()
    ots = OptionTransaction.objects.filter(
        option_plan__company=company,
        vesting_months__gt=0).distinct()
    header = [_('full name'), _('count'), _('security'),
              _('is management member'),
              _('vesting in months'), _('asset type')]
    _rows = []
    _rows += [
        [p.buyer.get_full_name(), p.count, unicode(p.security),
         p.buyer.is_management, p.vesting_months, _('stock')
         ] for p in positions]
    _rows += [[ot.buyer.get_full_name(), ot.count,
              unicode(ot.option_plan.security),
              ot.buyer.is_management,
              ot.vesting_months, _('certificate')] for ot in ots]

    rows = []
    for row in _rows:
        rows.append([to_string_or_empty(s) for s in row])

    save_to_excel_file(filename, rows, header, response=response)

    return response


class IndexView(TemplateView):

    template_name = 'reports/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['company'] = get_company_from_request(self.request)
        return context
