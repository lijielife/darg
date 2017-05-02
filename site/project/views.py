import csv
import datetime
import logging
import time

import dateutil.parser
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.flatpages.models import FlatPage
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden)
from django.shortcuts import get_object_or_404, redirect, resolve_url
from django.template import loader
from django.utils.text import slugify
from django.utils.translation import ugettext as _
from zinnia.models.entry import Entry

from project.tasks import send_initial_password_mail
from services.instapage import InstapageSubmission as Instapage
from shareholder.models import (Company, Operator, OptionTransaction, Position,
                                Security, Shareholder)
from utils.pdf import render_to_pdf_response
from utils.session import get_company_from_request

logger = logging.getLogger(__name__)


def _check_subscription(request):
    company = get_company_from_request(request, fail_silently=True)
    if company:
        customer = company.get_customer()
        if customer and not customer.has_active_subscription():
            redirect_url = resolve_url(
                'djstripe:subscribe',
                **dict(company_id=company.pk)
            )
            return redirect(redirect_url)

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


def index(request):
    template = loader.get_template('index.html')
    context = {}
    if Entry.published.all().exists():
        context['latest_blog_entry'] = Entry.published.all()[0]
    context['flatpages'] = FlatPage.objects.all()
    context['company_count'] = Company.objects.count()
    context['shareholder_count'] = Shareholder.objects.count()
    return HttpResponse(template.render(context=context, request=request))


@login_required
def start(request):
    subscription_redirect = _check_subscription(request)
    if subscription_redirect:
        return subscription_redirect

    template = loader.get_template('start.html')
    return HttpResponse(template.render(request=request))


def instapage(request):
    """
    import user data from instapage
    instapage?submission=30122798
    create user and login
    """
    if not request.GET.get('submission'):
        return HttpResponseBadRequest('invalid data')

    # get and extract data
    sub = int(request.GET.get('submission'))
    instapage = Instapage()
    instapage.get(sub)
    name = instapage._get_value_by_field_name('Name').split(' ')
    email = instapage._get_value_by_field_name('Email')
    ip = instapage._get_value_by_field_name('ip')
    password = User.objects.make_random_password()

    if len(name) == 2:
        first_name, last_name = name
    elif len(name) == 1:
        first_name, last_name = '', name[0]
    else:
        first_name, last_name = name[0], ' '.join(name[1:])

    kwargs = dict(
        first_name=first_name, last_name=last_name, email=email,
        is_active=True, username=email[:29],
        )

    # save data
    user, created = User.objects.get_or_create(
        email=kwargs.get('email'), defaults=kwargs)

    # user existing
    if not created:
        logger.warning('instapage user signed up twice', extra=kwargs)
        msg = _(u'You have already an existing user account. '
                'Please login or reset your password.')
        messages.add_message(request, messages.INFO, msg)
        return redirect(reverse('two_factor:login'))

    # new user
    user.set_password(password)
    user.save()
    profile = user.userprofile
    profile.ip = ip
    profile.tnc_accepted = True
    profile.save()

    # authenticate user
    user = authenticate(username=email, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)

        # send password email
        send_initial_password_mail.delay(user=user, password=password)
    else:
        logger.error('failed to authenticate new user',
                     extra={'user': user, 'kwargs': kwargs})

    return redirect(reverse('start'))


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


@login_required
def option_pdf(request, option_id):
    """
    generate pdf for option transaction/urkunde
    """
    # perm check
    if not Operator.objects.filter(
        user=request.user, company__optionplan__optiontransaction__id=option_id
    ).exists():
        return HttpResponseForbidden()

    option = get_object_or_404(OptionTransaction, id=option_id)
    company = option.option_plan.company

    response = render_to_pdf_response(
        'option.pdf.html',
        {
            'pagesize': 'A4',
            'company': company,
            'today': datetime.datetime.now(),
            'currency': 'CHF',
            'option': option,
        }
    )

    # Create the HttpResponse object with the appropriate PDF header.
    # if not DEBUG
    if not settings.DEBUG:
        response['Content-Disposition'] = (
            u'attachment; filename="'
            u'{}_option_{}_ID{}.pdf"'.format(
                time.strftime("%Y-%m-%d"), company.name, option.certificate_id)
        )

    if not option.printed_at:
        option.printed_at = datetime.datetime.now()
        option.save()

    return response


@login_required
def position_option_pdf(request, option_id):
    """
    print pdf for certificate depot for stocks
    """

    # perm check
    operator_qs = Operator.objects.filter(
        Q(company__shareholder__seller__id=option_id) |
        Q(company__shareholder__buyer__id=option_id),
        user=request.user
    )
    if not operator_qs.exists():
        return HttpResponseForbidden()

    position = get_object_or_404(Position, id=option_id)
    company = operator_qs.first().company

    response = render_to_pdf_response(
        'certificate.pdf.html',
        {
            'pagesize': 'A4',
            'company': company,
            'today': datetime.datetime.now(),
            'currency': 'CHF',
            'position': position,
        }
    )

    # Create the HttpResponse object with the appropriate PDF header.
    # if not DEBUG
    if not settings.DEBUG:
        response['Content-Disposition'] = (
            u'attachment; filename="'
            u'{}_option_{}_ID{}.pdf"'.format(
                time.strftime("%Y-%m-%d"), company.name,
                position.certificate_id)
        )

    if not position.printed_at:
        position.printed_at = datetime.datetime.now()
        position.save()

    return response
