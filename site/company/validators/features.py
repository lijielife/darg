
import logging

from django.conf import settings
from django.core.validators import MaxValueValidator
from django.utils.translation import ugettext_lazy as _

from .base import BaseCompanyValidator


logger = logging.getLogger(__name__)


class ShareholderCountPlanValidator(BaseCompanyValidator):
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
    code = 'shareholders'

    def __call__(self, plan_name):
        plan = settings.DJSTRIPE_PLANS.get(plan_name)
        if not plan:
            raise ValueError(
                'Could not find a plan named "{}"'.format(plan_name))

        shareholders_feature = plan.get('features', {}).get('shareholders', {})
        max_shareholder_count = shareholders_feature.get('max')
        # FIXME: use company.shareholder_count for only active shareholders?
        shareholder_count = self.company.shareholder_set.count()
        if (max_shareholder_count and
                shareholder_count > max_shareholder_count):
            error_message = self.message.format(
                **dict(count=shareholder_count,
                       max_shareholders=max_shareholder_count))
            self.raise_execption(error_message, code=self.code)


class SecurityCountPlanValidator(BaseCompanyValidator):
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
    code = 'securities'

    def __call__(self, plan_name):
        plan = settings.DJSTRIPE_PLANS.get(plan_name)
        if not plan:
            raise ValueError(
                'Could not find a plan named "{}"'.format(plan_name))

        security_feature = plan.get('features', {}).get('securities', {})
        max_security_count = security_feature.get('max')
        security_count = self.company.security_set.count()
        if max_security_count and security_count > max_security_count:
            error_message = self.message.format(
                **dict(count=security_count,
                       max_securities=max_security_count,)),
            self.raise_execption(error_message[0], code=self.code)


class ShareholderCreateMaxCountValidator(BaseCompanyValidator):
    """
    check if given company subscription allow addition of shareholder
    """

    def __call__(self):
        # FIXME: use company.shareholder_count for only active shareholders?
        company_shareholders = self.company.shareholder_set.count()
        plan = settings.DJSTRIPE_PLANS.get(
            self.company.get_current_subscription_plan(), {})
        shareholders_feature = plan.get('features', {}).get('shareholders', {})
        max_shareholders = shareholders_feature.get('max', None)
        if max_shareholders is not None:
            if company_shareholders + 1 > max_shareholders:
                logger.warning('cannot create more shareholders acc to subscr.'
                               ' plan.', extra={'plan': plan})
            validator = MaxValueValidator(max_shareholders)
            return validator(company_shareholders + 1)


class SecurityCreateMaxCountValidator(BaseCompanyValidator):
    """
    check if given company subscription allow addition of security
    """

    def __call__(self):
        # FIXME: use company.shareholder_count for only active shareholders?
        company_securities = self.company.security_set.count()
        plan = settings.DJSTRIPE_PLANS.get(
            self.company.get_current_subscription_plan(), {})
        security_feature = plan.get('features', {}).get('securities', {})
        max_securities = security_feature.get('max', None)
        if max_securities is not None:
            return MaxValueValidator(max_securities)(company_securities + 1)
