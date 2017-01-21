

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from .base import BaseCompanyValidator


class ShareholderCountValidator(BaseCompanyValidator):
    """
    check if company fulfills shareholder count requirement for given plan

    usage:
        ShareholderCountValidator(<company>)(<plan_name>)
    or
        validator = ShareholderCountValidator(<company>)
        validator(<plan_name>)
    """

    message = _('Too many shareholders are registered ({count}).'
                ' (max: {max_shareholders})')
    code = 'shareholder_count'

    def __call__(self, plan_name):
        plan = settings.DJSTRIPE_PLANS.get(plan_name)
        if not plan:
            raise ValueError(
                'Could not find a plan named "{}"'.format(plan_name))

        shareholder_feature = plan.get('features', {}).get('shareholders', {})
        max_shareholder_count = shareholder_feature.get('count')
        shareholder_count = self.company.shareholder_count()
        if (max_shareholder_count
                and shareholder_count > max_shareholder_count):
            error_message = self.message.format(
                **dict(max_shareholder=max_shareholder_count,
                       count=shareholder_count))
            self.raise_execption(error_message, code=self.code)


class SecurityCountValidator(BaseCompanyValidator):
    """
    check if company fulfills security count requirement for given plan

    usage:
        SecurityCountValidator(<company>)(<plan_name>)
    or
        validator = SecurityCountValidator(<company>)
        validator(<plan_name>)
    """

    message = _('Too many securities in use ({count}).'
                ' (max: {max_securities})')
    code = 'security_count'

    def __call__(self, plan_name):
        plan = settings.DJSTRIPE_PLANS.get(plan_name)
        if not plan:
            raise ValueError(
                'Could not find a plan named "{}"'.format(plan_name))

        security_feature = plan.get('features', {}).get('securities', {})
        max_security_count = security_feature.get('count')
        security_count = self.company.security_set.count()
        if max_security_count and security_count > max_security_count:
            error_message = self.message.format(
                **dict(max_securities=max_security_count,
                       count=security_count)),
            self.raise_execption(error_message[0], code=self.code)
