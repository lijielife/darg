
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

    street = models.CharField(_('Street'), max_length=255, blank=True,
                              null=True)
    city = models.CharField(_('City'), max_length=255, blank=True, null=True)
    province = models.CharField(_('Province'), max_length=255, blank=True,
                                null=True)
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
        return self.street and self.city and self.postal_code and self.country
