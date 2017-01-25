import csv
import datetime
import logging
import time

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.flatpages.models import FlatPage
from django.core.urlresolvers import reverse
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden)
from django.shortcuts import get_object_or_404, redirect
from django.template import RequestContext, loader
from django.utils.text import slugify
from django.utils.translation import ugettext as _
from zinnia.models.entry import Entry

from project.tasks import send_initial_password_mail
from services.instapage import InstapageSubmission as Instapage
from shareholder.models import Company, Operator
from utils.formatters import human_readable_segments
from utils.pdf import render_to_pdf

logger = logging.getLogger(__name__)


def _get_contacts(company):

    rows = []
    rows.append([
        _(u'shareholder number'), _(u'last name'), _(u'first name'),
        _(u'email'),
        _(u'language ISO'), _('language full'), _('street'), _('street 2'),
        _('c/o'), _('city'), _('zip'), _('country'), _('nationality'),
        _('pobox'), _('mailing type'),
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
            shareholder.user.userprofile.country.name,
            shareholder.user.userprofile.pobox,
            shareholder.get_mailing_type_display()
        ]
        if shareholder.user.userprofile.nationality:
            row.append([shareholder.user.userprofile.nationality.name])
        rows.append([row])

    return rows

def index(request):
    template = loader.get_template('index.html')
    context = RequestContext(request, {})
    if Entry.published.all().exists():
        context['latest_blog_entry'] = Entry.published.all()[0]
    context['flatpages'] = FlatPage.objects.all()
    return HttpResponse(template.render(context))


@login_required
def start(request):
    template = loader.get_template('start.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))


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
def captable_csv(request, company_id):
    """ returns csv with active shareholders """

    # perm check
    if not Operator.objects.filter(
        user=request.user, company__id=company_id
    ).exists():
        return HttpResponseForbidden()

    company = get_object_or_404(Company, id=company_id)
    track_numbers_secs = company.security_set.filter(track_numbers=True)

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = (
        u'attachment; '
        u'filename="{}_captable_{}.csv"'.format(
            time.strftime("%Y-%m-%d"), slugify(company.name)
        ))

    writer = csv.writer(response)

    header = [
        _(u'shareholder number'), _(u'last name'), _(u'first name'),
        _(u'email'), _(u'share count'), _(u'votes share percent'),
        _(u'language ISO'), _('language full')]

    if track_numbers_secs.exists():
        header.append(_('Share IDs'))

    writer.writerow(header)

    for shareholder in company.get_active_shareholders():
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
        if track_numbers_secs.exists():
            text = ""
            for sec in track_numbers_secs:
                text += "{}: {} ".format(
                    sec.get_title_display(),
                    human_readable_segments(shareholder.current_segments(sec) or
                                            _('None'))
                )
            row.append(text)
        writer.writerow([unicode(s).encode("utf-8") for s in row])

    return response


@login_required
def captable_pdf(request, company_id):

    # perm check
    if not Operator.objects.filter(
        user=request.user, company__id=company_id
    ).exists():
        return HttpResponseForbidden()

    company = get_object_or_404(Company, id=company_id)

    response = render_to_pdf(
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

    # Create the HttpResponse object with the appropriate PDF header.
    # if not DEBUG
    if not settings.DEBUG:
        response['Content-Disposition'] = (
            u'attachment; filename="'
            u'{}_captable_{}.pdf"'.format(
                time.strftime("%Y-%m-%d"), company.name)
        )

    return response
