
from django.shortcuts import get_object_or_404

from braces.views._access import AccessMixin

from shareholder.models import Company


class PaymentViewCompanyObjectMixin(object):
    """
    mixin for payment (djstripe) views to get company object from request kwarg
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
