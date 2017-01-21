
from decimal import Decimal

from django import template
from django.conf import settings
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


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


@register.assignment_tag
def get_plan_price_per_shareholder(plan_data):
    plan = settings.DJSTRIPE_PLANS.get(plan_data.get('plan'))
    if not plan:
        return

    shareholder_feature = plan.get('features', {}).get('shareholders', {})
    return shareholder_feature.get('price')


@register.assignment_tag
def get_invoice_currency(invoice):
    """
    return currency for invoice if all invoice items have same currency
    """
    item_currencies = invoice.items.all().values_list('currency', flat=True)
    if len(set(item_currencies)) == 1:
        return item_currencies[0].upper()


@register.filter
def has_shareholderstatement_reports(user):
    """
    checks if user is operator for company(s) and if any reports are available
    """
    from shareholder.models import ShareholderStatementReport
    company_ids = user.operator_set.values_list('company_id', flat=True)
    # TODO: check company subscription
    qs = ShareholderStatementReport.objects.filter(company__in=company_ids)
    return bool(qs.count())


@register.assignment_tag
def get_plan_features(plan_name):
    """
    get all features for plan
    dictionary with 'core' and 'features' keys
    """
    features = dict(core=[], features=[])
    plan = settings.DJSTRIPE_PLANS.get(plan_name)
    if not plan:
        return features

    plan_features = plan.get('features')
    annotations = 0
    for name in settings.SUBSCRIPTION_FEATURES.keys():
        subscription_feature = settings.SUBSCRIPTION_FEATURES.get(name, {})
        plan_feature = plan_features.get(name, {})
        if subscription_feature.get('core'):
            key = 'core'
            if name == 'securities':
                title = u''
                security_count = plan_feature.get('count')
                security_price = plan_feature.get('price')
                if security_count:
                    label = (security_count == 1 and _('Security')
                             or _('Securities'))
                    title += u'{} {}'.format(security_count, label)
                if security_price:  # NOTE: we assuming a valid number
                    if title:
                        title += '\n'
                    title += _(
                        'More securities: CHF +{amount:.2f} / M.').format(
                            **dict(amount=security_price / 100)
                    )
                if not security_count and not security_price:
                    title = subscription_feature['title']
                subscription_feature['title'] = title
            else:
                subscription_feature['highlight'] = (
                    plan_feature.get('count') or _('Unlimited'))
        else:
            key = 'features'
        if subscription_feature.get('annotation'):
            annotations += 1
            subscription_feature['annotation_marker'] = '*' * annotations

        subscription_feature['exclude'] = name not in plan_features

        features[key].append(subscription_feature)

    return features


@register.assignment_tag
def get_plans_annotations():
    """
    return all annotations for subscription plans
    """
    annotations = []
    annotation_count = 0
    for feature_name, feature in settings.SUBSCRIPTION_FEATURES.items():
        if feature.get('annotation'):
            annotation_count += 1
            annotation = dict(
                title=feature.get('annotation'),
                marker='*' * annotation_count
            )
            annotations.append(annotation)
    return annotations


@register.simple_tag
def invoice_get_vat_css_class(item_count):
    """
    return 'odd' or 'even'
    """
    return item_count % 2 and 'even' or 'odd'


@register.simple_tag
def invoice_get_total_css_class(item_count, vat_included):
    """
    return 'odd' or 'even'
    """
    if vat_included:
        item_count += 1
    return invoice_get_vat_css_class(item_count)
