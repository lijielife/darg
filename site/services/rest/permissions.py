
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

from rest_framework import permissions


class IsOperatorPermission(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        is_authenticated = super(IsOperatorPermission, self).has_permission(
            request, view)
        return is_authenticated and request.user.operator_set.count()


class HasSubscriptionPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        """
        check company subscription
        """
        company = self._get_company(request)
        if not company:
            # FIXME: what now? True or False?
            return False

        plan_name = company.get_current_subscription_plan()

        if not plan_name:
            # FIXME: what now? True or False?
            return False

        subscription_features = getattr(view, 'subscription_features', [])
        if not subscription_features:
            return True

        plan = settings.DJSTRIPE_PLANS.get(plan_name, {})
        plan_features = plan.get('features', {})
        for feature in subscription_features:
            if feature not in plan_features:
                self.message = {feature: _('Feature not supported.')}
                return False

            feature_config = plan_features.get(feature, {})
            if not feature_config:
                continue

            # got config
            validators = feature_config.get('validators', {})
            action = getattr(view, 'action', '')
            for validator in validators.get(action, []):
                validator_class = import_string(validator)
                try:
                    validator_class(company)()
                except ValidationError as err:
                    self.message = {feature: err.messages}
                    return False

        return True

    def has_object_permission(self, request, view, obj=None):
        # TODO?!
        return True

    def _get_company(self, request):
        """
        get company from request
        """
        # TODO: the company must be delivered with the request data!
        #       for now: use company of first operator of user
        if hasattr(request, 'user') and request.user.is_authenticated():
            operator = request.user.operator_set.first()
            return operator and operator.company
