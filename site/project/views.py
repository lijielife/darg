import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.flatpages.models import FlatPage
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, resolve_url
from django.template import loader
from django.utils.translation import ugettext as _
from zinnia.models.entry import Entry

from project.tasks import send_initial_password_mail
from services.instapage import InstapageSubmission as Instapage
from shareholder.models import Company, Shareholder
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
