import logging
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

from rest_framework import permissions
from utils.session import get_company_from_request

logger = logging.getLogger(__name__)


class SafeMethodsOnlyPermission(permissions.BasePermission):
    """Only can access non-destructive methods (like GET and HEAD)"""
    def has_permission(self, request, view):
        return self.has_object_permission(request, view)

    def has_object_permission(self, request, view, obj=None):
        return request.method in permissions.SAFE_METHODS


class IsOperatorPermission(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        is_authenticated = super(IsOperatorPermission, self).has_permission(
            request, view)
        company = get_company_from_request(request, fail_silently=True)
        return (is_authenticated and
                company and
                request.user.operator_set.filter(company=company).exists())


class HasSubscriptionPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        """
        check company subscription
        """
        company = get_company_from_request(request, fail_silently=True)
        if not company:
            return False

        plan_name = company.get_current_subscription_plan()

        if not plan_name:
            # FIXME: what now? True or False?
            return False

        subscription_features = getattr(view, 'subscription_features', [])
        if not subscription_features:
            return True

        plan = settings.DJSTRIPE_PLANS.get(plan_name, {})
        if not plan:
            logger.error('plan lookup in rest api permissions failed',
                         extra={'plan_name': plan_name,
                                'DJSTRIPE_PLANS': settings.DJSTRIPE_PLANS})
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


class UserCanAddCompanyPermission(SafeMethodsOnlyPermission):
    """Allow everyone which is not a shareholder nor an operator yet to
    add a company
    """
    def has_object_permission(self, request, view, obj=None):

        can_add = False
        if obj is None:
            # Either a list or a create, so no author
            can_add = True
        return can_add or super(
            UserCanAddCompanyPermission, self).has_object_permission(
                request, view, obj)
