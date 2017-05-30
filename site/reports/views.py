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


XLSX_CONTENT_TYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  # noqa


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


class IndexView(TemplateView):

    template_name = 'reports/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['company'] = get_company_from_request(self.request)
        return context
