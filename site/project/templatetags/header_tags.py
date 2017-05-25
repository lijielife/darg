
from django import template

from utils.session import get_company_from_request


register = template.Library()


@register.assignment_tag
def get_company_initials(request):
    """
    return string company initials
    """
    company = get_company_from_request(request)
    initials = u''.join([part[0]for part in company.name.split(' ')])
    return initials.upper()
