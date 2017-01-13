
from django.core.validators import EmailValidator
from django.utils.translation import ugettext_lazy as _

from .base import BaseCompanyValidator


class CompanyEmailRequired(BaseCompanyValidator):
    """
    check if company has a valid email address set

    usage:
        CompanyEmailRequired(<company>)(<email>)
    or
        validator = CompanyEmailRequired(<company>)
        validator(<email>)
    """

    code = 'email'

    def __call__(self, plan):
        # check for validity
        EmailValidator(code=self.code)(self.company.email)


class CompanyAddressRequired(BaseCompanyValidator):
    """
    check if company has an address set (no validity check ... for now)
    usage:
        CompanyAddressRequired(<company>)()
    or
        validator = CompanyAddressRequired(<company>)
        validator()
    """

    code = None
    message = _('An address is required.')

    def __call__(self, plan=None):
        if not self.company.has_address:
            self.raise_execption(self.message, code=self.code)
