
# FIXME: maybe move this module to shareholder app (model lives there)

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from shareholder.models import Company


class BaseCompanyValidator(object):

    def __init__(self, company):
        if not isinstance(company, Company):
            raise ValueError(_('company must be instance of {}').format(
                Company._meta.label))
        self.company = company

    def raise_execption(self, message, code=None):
        raise ValidationError(message, code=code)

    def raise_error(self, message, code=None):
        return self.raise_execption(message, code=code)
