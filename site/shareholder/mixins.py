
from django.contrib.auth import login, logout, decorators as auth_decorators
from django.db import models
from django.utils.translation import ugettext_lazy as _

from rest_framework.authtoken.models import Token


class AuthTokenLoginViewMixin(object):
    """
    checks if a authentication token was sent and authenticate the user with it
    """

    login_user = True

    def dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(),
                              self.http_method_not_allowed)
            # check for auth token
            key = getattr(request, request.method, {}).get('token')
            token = Token.objects.filter(key=key).first()
            if token and token.user.is_active:
                if self.login_user:
                    # log the user in
                    token.user.backend = (
                        'django.contrib.auth.backends.ModelBackend')
                    login(request, token.user)
                else:
                    # just set the user for this request
                    request.user = token.user
            elif key:
                # there is a token present but login could not be done
                logout(request)

            # remove token from query
            if 'token' in request.META.get('QUERY_STRING', ''):
                del request.META['QUERY_STRING']

            if getattr(self, 'login_required', False):
                handler = auth_decorators.login_required(handler)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)


class AuthTokenSingleViewMixin(AuthTokenLoginViewMixin):
    """
    works like AuthTokenLoginViewMixin, but authentication works only for
    single request (does not log the user in)
    """

    login_user = False


class AddressModelMixin(models.Model):
    """
    add fields street, postal_code, city, province, country to model
    """
    ADDRESS_FIELDS = ('street', 'street2', 'city', 'province', 'pobox', 'c_o',
                      'postal_code', 'country')
    REQUIRED_ADDRESS_FIELDS = ('street', 'city', 'postal_code', 'country')
    STRIPE_FIELD_MAPPING = {
        'address_line1': 'street',
        'address_line2': 'street2',
        'address_zip': 'postal_code',
        'address_city': 'city',
        'address_state': 'province'
        # 'address_country': 'country',
    }

    street = models.CharField(_('Street'), max_length=255, blank=True,
                              null=True)
    street2 = models.CharField(_('Street 2'), max_length=255, blank=True,
                               null=True)
    city = models.CharField(_('City'), max_length=255, blank=True, null=True)
    province = models.CharField(_('Province'), max_length=255, blank=True,
                                null=True)
    pobox = models.CharField(_('PO Box'), max_length=255, blank=True,
                             null=True)
    c_o = models.CharField(_('C/O'), max_length=255, blank=True, null=True)
    postal_code = models.CharField(_('Postal code'), max_length=255,
                                   blank=True, null=True)
    country = models.ForeignKey('shareholder.Country', blank=True, null=True,
                                verbose_name=_('Country'))

    class Meta:
        abstract = True

    @property
    def has_address(self):
        """
        return True if street, city, postal_code and country field are set
        """
        return all(getattr(self, fn) for fn in self.REQUIRED_ADDRESS_FIELDS)

    def read_address_from_stripe_object(self, stripe_data, save=True):
        """
        update address information for object from stripe data
        """
        if not stripe_data:
            return

        for key, fieldname in self.STRIPE_FIELD_MAPPING.items():
            setattr(self, fieldname, stripe_data.get(key, ''))

        country_name = stripe_data.get('address_country')
        if country_name:
            # try to fetch country object
            country_field = self._meta.get_field('country')
            Country = country_field.related_model
            self.country = Country.objects.filter(
                name__iexact=country_name).first()

        if save:
            self.save()


class ShareholderStatementReportViewMixin(object):
    """
    mixin for shareholder statement report views
    """

    subscription_features = ['shareholder_statements']

    def get_user_companies(self):
        from shareholder.models import Company
        if not self.request.user.is_authenticated():
            return Company.objects.none()
        return Company.objects.filter(operator__user=self.request.user)

    def get_queryset(self):
        from shareholder.models import ShareholderStatementReport
        qs = ShareholderStatementReport.objects.filter(
            company__in=self.get_company_pks())
        return qs.order_by('company__name', '-report_date')
