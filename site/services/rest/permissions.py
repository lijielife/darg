
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.module_loading import import_string

from rest_framework import permissions


class SafeMethodsOnlyPermission(permissions.BasePermission):
    """Only can access non-destructive methods (like GET and HEAD)"""
    def has_permission(self, request, view):
        return self.has_object_permission(request, view)

    def has_object_permission(self, request, view, obj=None):
        return request.method in permissions.SAFE_METHODS


class UserCanAddCompanyPermission(SafeMethodsOnlyPermission):
    """Allow everyone which is not a shareholder nor an operator yet to add a company"""
    def has_object_permission(self, request, view, obj=None):

        can_add = False
        if obj is None:
            # Either a list or a create, so no author
            can_add = True
        return can_add or super(UserCanAddCompanyPermission, self).has_object_permission(request, view, obj)


class UserCanEditCompanyPermission(permissions.BasePermission):
    """Allow everyone which is not a shareholder nor an operator yet to add a company"""
    def has_object_permission(self, request, view, obj=None):

        can_add = False
        if obj is None:
            # Either a list or a create, so no author
            can_add = True
        return can_add or super(
            UserCanEditCompanyPermission, self
        ).has_object_permission(request, view, obj)


class UserIsOperatorPermission(permissions.BasePermission):
    """
    Only operators of the same company may edit
    """
    def has_object_permission(self, request, view, obj=None):

        if hasattr(obj, 'company'):
            company = obj.company
        elif hasattr(obj.buyer, 'company'):
            company = obj.buyer.company
        elif hasattr(obj.seller, 'company'):
            company = obj.seller.company

        return request.user.operator_set.filter(company=company).exists()


class UserCanAddShareholderPermission(SafeMethodsOnlyPermission):
    """Allow everyone to add a company"""
    def has_object_permission(self, request, view, obj=None):

        return request.user.operator_set.filter(company=obj.company).exists()


class UserCanAddPositionPermission(SafeMethodsOnlyPermission):
    """Allow everyone to add a company"""
    def has_object_permission(self, request, view, obj=None):
        can_add = False
        if obj is None:
            # Either a list or a create, so no author
            can_add = True
        return can_add or super(UserCanAddPositionPermission, self).has_object_permission(request, view, obj)


class UserCanAddOptionPlanPermission(SafeMethodsOnlyPermission):
    """Allow everyone to add a company"""
    def has_object_permission(self, request, view, obj=None):
        can_add = False
        if obj is None:
            # Either a list or a create, so no author
            can_add = True
        return can_add or super(UserCanAddOptionPlanPermission, self).has_object_permission(request, view, obj)


class UserCanAddOptionTransactionPermission(SafeMethodsOnlyPermission):
    """Allow everyone to add a company"""
    def has_object_permission(self, request, view, obj=None):
        can_add = False
        if obj is None:
            # Either a list or a create, so no author
            can_add = True
        return can_add or super(UserCanAddOptionTransactionPermission, self).has_object_permission(request, view, obj)


class UserCanAddInviteePermission(SafeMethodsOnlyPermission):
    """Allow everyone to add a company"""
    def has_object_permission(self, request, view, obj=None):
        can_add = False
        if obj is None:
            # Either a list or a create, so no author
            can_add = True
        return can_add or super(UserCanAddInviteePermission, self).has_object_permission(request, view, obj)


class SubscriptionPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        """
        check company subscription
        """
        if not view.subscription_features:
            return True

        company = self._get_company(request)
        if not company:
            # FIXME: what now? True or False?
            return True

        plan_name = company.get_current_subscription_plan()

        if not plan_name:
            # FIXME: what now? True or False?
            return True

        plan = settings.DJSTRIPE_PLANS.get(plan_name, {})
        plan_features = plan.get('features', {})
        for feature in view.subscription_features:
            feature_config = plan_features.get(feature, {})
            if not feature_config:
                continue

            # got config
            validators = feature_config.get('validators', {})
            action_validators = validators.get(view.action, [])
            for validator in action_validators:
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
        if request.user and request.user.is_authenticated():
            operator = request.user.operator_set.first()
            return operator and operator.company
