import csv
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
from shareholder.models import (Company, Operator, OptionTransaction, Position,
                                Security)
from utils.session import get_company_from_request


def _get_contacts(company):

    rows = []
    rows.append([
        _(u'shareholder number'), _(u'last name'), _(u'first name'),
        _(u'email'),
        _(u'language ISO'), _('language full'), _('street'), _('street 2'),
        _('c/o'), _('city'), _('zip'), _('country'),
        _('pobox'), _('mailing type'), _('nationality'),
    ])

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
    rows.append([
        _(u'date'), _(u'buyer'), _(u'seller'),
        _(u'count'),
        _(u'value'), _('security'), _('comment'), _('depot type'),
        _('stock book id'), _(u'vesting period (options only'),
        _(u'cert id (options only)'),
    ])

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


def assembly_participation_csv(request, company_id):
    """ download csv with company participation list """
    company = get_object_or_404(Company, id=company_id)
    if company.operator_set.filter(user=request.user).exists():

        filename = u"assembly_participants_{}".format(slugify(company.name))
        header = [_('Shareholder#'), _('Full Name'), _('Address'),
                  _('share count'), _('capital'), _('vote count')]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}'.format(
            filename)

        writer = csv.writer(response)
        writer.writerow([unicode(s).encode("utf-8") for s in header])
        for shareholder in company.get_active_shareholders().order_by('number'):

            row = [shareholder.number, shareholder.get_full_name(),
                   shareholder.user.userprofile.get_address(),
                   shareholder.share_count(),
                   shareholder.cumulated_face_value(),
                   shareholder.vote_count()]
            writer.writerow([unicode(s).encode("utf-8") for s in row])

        return response

    else:
        return HttpResponseForbidden(_("Permission denied"))


@login_required
def contacts_csv(request, company_id):
    """ returns csv with active shareholders """

    # perm check
    if not Operator.objects.filter(
        user=request.user, company__id=company_id
    ).exists():
        return HttpResponseForbidden()

    company = get_object_or_404(Company, id=company_id)

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = (
        u'attachment; '
        u'filename="{}_contacts_{}.csv"'.format(
            time.strftime("%Y-%m-%d"), slugify(company.name)
        ))

    writer = csv.writer(response)

    rows = _get_contacts(company)
    for row in rows:
        writer.writerow([unicode(s).encode("utf-8") for s in row])

    return response


@login_required
def transactions_csv(request, company_id):
    """ returns csv with transactions """

    # perm check
    if not Operator.objects.filter(
        user=request.user, company__id=company_id
    ).exists():
        return HttpResponseForbidden()

    company = get_object_or_404(Company, id=company_id)
    security = get_object_or_404(Security, id=request.GET.get('security'))
    from_date = dateutil.parser.parse(request.GET.get('from'))
    to_date = dateutil.parser.parse(request.GET.get('to'))

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = (
        u'attachment; '
        u'filename="{}_transactions_{}_.csv"'.format(
            time.strftime("%Y-%m-%d"), slugify(company.name),
            slugify(security.get_title_display())
        ))

    writer = csv.writer(response)

    rows = _get_transactions(from_date, to_date, security, company)
    for row in rows:
        writer.writerow([unicode(s).encode("utf-8") for s in row])

    return response


@login_required
def printed_certificates_csv(request, company_id):
    """
    return csv with list of printed certificates
    """
    # perm check
    if not Operator.objects.filter(
        user=request.user, company__id=company_id
    ).exists():
        return HttpResponseForbidden()

    company = get_object_or_404(Company, id=company_id)

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = (
        u'attachment; '
        u'filename="{}_printed_certificates_{}.csv"'.format(
            time.strftime("%Y-%m-%d"), slugify(company.name)
        ))

    writer = csv.writer(response)

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
    rows = [[_('full name'), _('share count'), _('security name'),
             _('certificate id'), _('certificate printed at'),
             _('security type')]]
    # add option transactions
    rows += [
        [ot.buyer.get_full_name(),
         ot.count,
         unicode(ot.option_plan.security),
         ot.certificate_id,
         ot.printed_at, _('option')]
        for ot in ots]
    # add positions
    rows += [
        [ot.buyer.get_full_name(),
         ot.count,
         unicode(ot.security),
         ot.certificate_id,
         ot.printed_at, _('stock')]
        for ot in pos]
    # render csv
    for row in rows:
        writer.writerow([unicode(s).encode("utf-8") for s in row])

    return response


@login_required
def vested_csv(request, company_id):
    """
    return csv with list of vested shareholders and positions
    """
    # perm check
    if not Operator.objects.filter(
        user=request.user, company__id=company_id
    ).exists():
        return HttpResponseForbidden()

    company = get_object_or_404(Company, id=company_id)

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = (
        u'attachment; '
        u'filename="{}_vested_{}.csv"'.format(
            time.strftime("%Y-%m-%d"), slugify(company.name)
        ))

    writer = csv.writer(response)

    positions = Position.objects.filter(
        Q(buyer__company=company) | Q(seller__company=company),
        vesting_months__gt=0).distinct()
    ots = OptionTransaction.objects.filter(
        option_plan__company=company,
        vesting_months__gt=0).distinct()
    rows = [[_('full name'), _('count'), _('security'),
             _('is management member'),
            _('vesting in months'), _('asset type')]]
    rows += [
        [p.buyer.get_full_name(), p.count, unicode(p.security),
         p.buyer.is_management, p.vesting_months, _('stock')
         ] for p in positions]
    rows += [[ot.buyer.get_full_name(), ot.count,
              unicode(ot.option_plan.security),
              ot.buyer.is_management,
              ot.vesting_months, _('certificate')] for ot in ots]
    for row in rows:
        writer.writerow([unicode(s).encode("utf-8") for s in row])

    return response


class IndexView(TemplateView):

    template_name = 'reports/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['company'] = get_company_from_request(self.request)
        return context
