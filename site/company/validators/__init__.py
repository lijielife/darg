
from django.core.validators import EmailValidator

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
