
from django import template
from django.utils.timezone import now


register = template.Library()


@register.filter
def user_name(user):
    """
    get full name or email of user
    """
    return user.get_full_name() or user.email


# shareholder assets

@register.assignment_tag
def get_shareholder_assets(shareholder, date=None):
    securities = shareholder.company.security_set.all()
    result_list = list()
    for sec in securities:
        count = shareholder.share_count(security=sec, date=date) or 0
        if count:
            result_list.append(dict(
                name=sec.get_title_display(),
                count=count,
                date=date or now().date(),
                value=sec.face_value
            ))
    return result_list


@register.assignment_tag
def get_share_value(shareholder, date=None):
    return shareholder.share_value(date=date)


@register.assignment_tag
def get_share_percent(shareholder, date=None):
    return shareholder.share_percent(date=date)


# shareholder options

@register.assignment_tag
def get_shareholder_options(shareholder, date=None):
    optionplans = shareholder.company.optionplan_set.all()
    result_list = list()
    for op in optionplans:
        count = shareholder.options_count(security=op.security, date=date) or 0
        if count:
            result_list.append(dict(
                name=op.security.get_title_display(),
                count=count,
                date=date or now().date(),
                value=op.exercise_price
            ))
    return result_list


@register.assignment_tag
def get_options_value(shareholder, date=None):
    return shareholder.options_value(date=date)


@register.assignment_tag
def get_options_percent(shareholder, date=None):
    return shareholder.options_percent(date=date)
