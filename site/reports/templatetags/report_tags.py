
from django import template

from reports.tasks import _order_queryset


register = template.Library()


# shareholder assets
@register.assignment_tag
def get_active_shareholders(security, date, ordering):
    qs = security.company.get_active_shareholders(date=date, security=security)
    result = _order_queryset(qs, ordering)
    return result


@register.assignment_tag
def get_active_option_holders(security, date, ordering):
    kwargs = dict(date=date, security=security)
    qs = security.company.get_active_option_holders(**kwargs)
    result = _order_queryset(qs, ordering)
    return result
