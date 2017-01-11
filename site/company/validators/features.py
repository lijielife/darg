

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

    def __call__(self, plan):
        plan_config = settings.PLAN_FEATURE_CONFIG.get(plan, {})
        max_shareholder_count = plan_config.get('shareholder_count')
        shareholder_count = self.company.shareholder_count()
        if (max_shareholder_count
                and max_shareholder_count < shareholder_count):
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

    def __call__(self, plan):
        plan_config = settings.PLAN_FEATURE_CONFIG.get(plan, {})
        max_security_count = plan_config.get('security_count')
        security_count = self.company.security_set.count()
        if max_security_count and max_security_count < security_count:
            error_message = self.message.format(
                **dict(max_securities=max_security_count,
                       count=security_count)),
            self.raise_execption(error_message[0], code=self.code)
