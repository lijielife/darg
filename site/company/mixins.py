
import collections

from django.apps import apps
from django.conf import settings
from django.shortcuts import get_object_or_404

from braces.views._access import AccessMixin

from shareholder.models import Company


class SubscriptionViewCompanyObjectMixin(object):
    """
    mixin for subscription (djstripe) views to get company object from request
    """

    def get_company(self):
        return get_object_or_404(Company, pk=self.kwargs.get('company_id'))


class CompanyOperatorPermissionRequiredViewMixin(AccessMixin):
    """
    view mixin to check if user is operator for company
    """

    def dispatch(self, request, *args, **kwargs):
        # login is required
        if not request.user.is_authenticated():
            return self.handle_no_permission(request)

        # check for company
        company = self.get_company()  # will throw 404 if not found
        operator_users = company.get_operators().values_list(
            'user_id', flat=True)
        # check if user is company operator
        if request.user.pk not in operator_users:
            return self.handle_no_permission(request)

        # good to go
        return (
            super(CompanyOperatorPermissionRequiredViewMixin, self).dispatch(
                request, *args, **kwargs))


class SubscriptionMixin(object):
    """
    mixin to check for subscription and plan features
    """

    def check_subscription(self, subscriber, features=None):
        """
        return boolean if subscriber has valid subscription
        also check for specific feature if given (str or list)
        """
        subscriber_model = apps.get_model(settings.DJSTRIPE_SUBSCRIBER_MODEL)
        if not isinstance(subscriber, subscriber_model):
            raise ValueError('subscriber must be of type {}'.format(
                subscriber_model))

        if not features:
            return subscriber.get_customer().has_active_subscription()

        if not isinstance(features, collections.Iterable):
            features = [features]

        return all(subscriber.has_feature_enabled(f) for f in features)
