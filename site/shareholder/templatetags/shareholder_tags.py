
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
def get_plan_price_per_shareholder(plan):
    plan_config = settings.PLAN_FEATURE_CONFIG.get(plan.get('plan'), {})
    return plan_config.get('shareholder_price')


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
    plan_features = settings.PLAN_FEATURES.get(plan_name, [])
    plan_features_config = settings.PLAN_FEATURE_CONFIG.get(plan_name, {})
    annotations = 0
    for name in settings.ORDERED_FEATURES:
        feature = settings.SUBSCRIPTION_FEATURES.get(name)
        if feature.get('core'):
            key = 'core'
            config = plan_features_config.get(name, {})
            if name is 'security_count':
                if config:
                    title = u'{} {}'.format(
                        config,
                        config == 1 and _('Security') or _('Securities')
                    )
                elif 'security_price' in plan_features_config.keys():
                    security_price = plan_features_config.get('security_price')
                    title = _('More securities: CHF +{amount} / M.').format(
                        **dict(amount=security_price / 100)
                    )
                else:
                    title = feature['title']
                feature['title'] = title
            else:
                feature['highlight'] = config or _('Unlimited')
        else:
            key = 'features'
        if feature.get('annotation'):
            annotations += 1
            feature['annotation_marker'] = '*' * annotations

        feature['exclude'] = name not in plan_features

        features[key].append(feature)

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
