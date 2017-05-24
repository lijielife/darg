
from django import template

from reports.tasks import _order_queryset


register = template.Library()


# shareholder assets
@register.assignment_tag
def get_active_shareholders(company, date, ordering, security=None):
    qs = company.get_active_shareholders(date=date, security=security)
    result = _order_queryset(qs, ordering)
    return result


@register.assignment_tag
def get_active_option_holders(company, date, ordering, security=None):
    kwargs = dict(date=date, security=security)
    qs = company.get_active_option_holders(**kwargs)
    result = _order_queryset(qs, ordering)
    return result


@register.assignment_tag
def shareholder_cumulated_face_value(shareholder, date):
    return shareholder.cumulated_face_value(date=date)
