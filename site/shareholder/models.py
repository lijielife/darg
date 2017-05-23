import logging
import math
import os
import re
import time
from collections import Counter
from decimal import Decimal

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.contrib.sites.models import Site
from django.core import signing
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q, Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import select_template
from django.utils import timezone
from django.utils.formats import date_format
from django.utils.module_loading import import_string
from django.utils.text import slugify
from django.utils.translation import activate as activate_lang
from django.utils.translation import ugettext as _
from django_languages import fields as language_fields
from djstripe.models import Customer as DjStripeCustomer
from natsort import natsorted
from rest_framework.authtoken.models import Token
from sorl.thumbnail import get_thumbnail
from tagging.models import Tag
from tagging.registry import register

from shareholder.mixins import DiscountedTaxByVestingModelMixin
from shareholder.validators import ShareRegisterValidator
from utils.formatters import (deflate_segments, flatten_list,
                              human_readable_segments, inflate_segments,
                              string_list_to_json)
from utils.files import human_readable_file_size
from utils.math import substract_list
from utils.pdf import render_pdf, merge_pdf

from .mixins import AddressModelMixin
from .validators import validate_remote_email_id

REGISTRATION_TYPES = [
    ('1', _('Personal ownership')),
    ('2', _('Personal representation')),
]

DEPOT_TYPES = [
    ('0', _('Zertifikatsdepot')),
    ('1', _('Gesellschaftsdepot')),
    ('2', _('Sperrdepot')),
]

MAILING_TYPES = [
    ('0', _('Not deliverable')),
    ('1', _('Postal Mail')),
    ('2', _('via Email')),
]

DISPO_SHAREHOLDER_TAG = 'dispo_shareholder'
TRANSFER_SHAREHOLDER_TAG = 'transfer_shareholder'

logger = logging.getLogger(__name__)


class TagMixin(object):
    """
    mixin to make tagging objects available inside models
    """
    def set_tag(self, tag):
        Tag.objects.update_tags(self, tag)

    def get_tags(self):
        return Tag.objects.get_for_object(self)


class CertificateMixin(models.Model):
    """
    bundling common certificate logic for transaction and optiontransaction
    """
    certificate_id = models.CharField(
        max_length=255, blank=True, null=True,
        help_text=_('id of the issued certificate'))
    printed_at = models.DateTimeField(_('was this printed at least once?'),
                                      blank=True, null=True)

    class Meta:
        abstract = True


class Country(models.Model):
    """Model for countries"""
    iso_code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=45, blank=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")
        ordering = ["name", "iso_code"]


class Bank(models.Model):
    """
    list of all swiss banks
    see https://goo.gl/i926Wr as guidance
    """
    short_name = models.CharField(max_length=15)
    name = models.CharField(max_length=60)
    postal_code = models.CharField(blank=True, max_length=10)
    address = models.CharField(blank=True, max_length=35)
    city = models.CharField(blank=True, max_length=35)
    swift = models.CharField(max_length=14, blank=True)
    bcnr = models.CharField(max_length=5)
    branchid = models.CharField(max_length=4)

    class Meta:
        verbose_name_plural = "Banks"
        ordering = ["name"]

    def __unicode__(self):
        return u'{}({}, {})'.format(self.name, self.city, self.swift)


def get_company_logo_upload_path(instance, filename):
    return os.path.join(
        "public", "company", "%d" % instance.id, "logo", filename)


def get_company_header_image_upload_path(instance, filename):
    return os.path.join(
        "public", "company", "%d" % instance.id, "header_image", filename)


class Company(AddressModelMixin, models.Model):

    name = models.CharField(max_length=255)
    share_count = models.PositiveIntegerField(blank=True, null=True)
    # country = models.ForeignKey(
    #     Country, null=True, blank=False, help_text=_("Headquarter location"))
    founded_at = models.DateField(
        _('Foundation date of the company'),
        null=True, blank=False)
    provisioned_capital = models.PositiveIntegerField(blank=True, null=True)
    logo = models.ImageField(
        blank=True, null=True,
        upload_to=get_company_logo_upload_path,)
    pdf_header_image = models.ImageField(
        blank=True, null=True,
        upload_to=get_company_header_image_upload_path,)
    vote_ratio = models.PositiveIntegerField(
        _('Voting rights calculation: one vote per X of security.face_value'),
        blank=True, null=True, default=1)
    signatures = models.CharField(
        _('comma separated list of board members permitted to sign in the name '
          'of the company'),
        max_length=255, blank=True)
    support_contact = models.CharField(
        _('string with comma separated names for support contact printed '
          'inside statement'),
        max_length=255, blank=True)
    email = models.EmailField(_('Email'), blank=True)  # required by djstripe

    is_statement_sending_enabled = models.BooleanField(
        _('Is statement sending enabled'), default=True)
    statement_sending_date = models.DateField(_('statement sending date'),
                                              null=True, blank=True)
    send_shareholder_statement_via_letter_enabled = models.BooleanField(
        _('Is sending the shareholder statement via snail mail enabled'),
        default=False)

    # pdf invoice
    invoice_template = 'pdf/invoice.pdf.html'  # shareholder/templates

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')

    def __unicode__(self):
        return u"{}".format(self.name)

    def _send_partial_share_rights_email(self, partials):
        """ send email with partial share after split list """
        operators = self.get_operators().values_list('user__email', flat=True)
        subject = _(
            u"Your list of partials for the share split for "
            u"company '{}'").format(self.name)
        message = _(
            "Dear Operator,\n\n"
            "Your share split has been successful. Please find the list of "
            "partial shares below:\n\n"
        )

        if len(partials) > 0:
            for id, part in partials.iteritems():
                s = Shareholder.objects.get(id=id)
                message = message + _(u"{}{}({}): {} shares\n").format(
                    s.user.first_name,
                    s.user.last_name,
                    s.user.email,
                    part,
                )
        else:
            message = message + _(u"--- No partial shares during split --- \n")

        message = message + _(
            "\nThese shareholders are eligible to either "
            "sell their partial shares or get compensated.\n\n"
            "Please handle them accordingly and update the share "
            "register.\n\n"
            "Your Share Register Team"
            )
        send_mail(
            subject, message, settings.SERVER_EMAIL,
            operators, fail_silently=False)
        logger.info(
            'split partials mail sent to operators: {}'.format(
                operators))

    # --- GETTER
    def shareholder_count(self):
        """ total count of active Shareholders """
        return Position.objects.filter(
            buyer__company=self, seller__isnull=True).count()

    def full_validate(self):
        """
        entry point for entire share register validation
        """
        validator = ShareRegisterValidator(self)
        return validator.is_valid()

    def get_active_shareholders(self, date=None, security=None):
        """ returns list of all active shareholders. this is a very expensive
        must use heavy caching"""
        cache_key = 'company-{}-{}-{}-active-shareholders'.format(
            self.pk, slugify((date or timezone.now().date()).isoformat()),
            slugify(security))
        cached = cache.get(cache_key)
        if cached:
            return Shareholder.objects.filter(pk__in=cached)

        kwargs = {}
        if date:
            kwargs.update({'date': date})
        if security:
            kwargs.update({'security': security})

        shareholder_list = []
        for shareholder in self.shareholder_set.all().order_by('number'):
            if shareholder.share_count(**kwargs) > 0:
                shareholder_list.append(shareholder.pk)

        result = Shareholder.objects.filter(
            pk__in=shareholder_list
        ).select_related(
            'user', 'user__userprofile', 'user__userprofile__country', 'company'
        ).order_by('number')

        # result can be large. memcache has 1MB cache limit... see
        # https://goo.gl/CFDsi3 for more details
        cache.set(cache_key, result.values_list('pk', flat=True), 60*60*24)
        return result

    def get_active_option_holders(self, date=None, security=None):
        """ returns list of all active shareholders """
        oh_list = []
        # get all users
        kwargs = dict(optiontransaction__isnull=False)
        if security:
            kwargs.update({'security': security})
        if date:
            kwargs.update({'optiontransaction__bought_at': date})
        sh_ids = self.optionplan_set.all().filter(**kwargs).values_list(
            'optiontransaction__buyer__id', flat=True).distinct()

        kwargs = {}
        if security:
            kwargs.update({'optionplan__security': security})
        if date:
            kwargs.update({'bought_at': date})

        for sh_id in sh_ids:
            sh = Shareholder.objects.get(id=sh_id)
            bought_options = sh.option_buyer.filter(**kwargs).aggregate(
                Sum('count'))
            sold_options = sh.option_seller.filter(**kwargs).aggregate(
                Sum('count'))
            if (
                (bought_options['count__sum'] or 0) -
                (sold_options['count__sum'] or 0) > 0
            ):
                oh_list.append(sh)
            elif (
                (bought_options['count__sum'] or 0) -
                (sold_options['count__sum'] or 0) < 0
            ):
                logger.error('user sold more options then he got',
                             extra={'shareholder': sh})
        return Shareholder.objects.filter(
            pk__in=[oh.pk for oh in oh_list]
        ).select_related(
            'user', 'user__userprofile', 'user__userprofile__country', 'company'
        )

    def get_all_option_plan_segments(self):
        """
        return list of number segments reserved for all option plans for
        this company
        """
        segments = self.optionplan_set.all().values_list(
            'number_segments', flat=True)
        return flatten_list(segments)

    def get_board_members(self):
        return self.signatures.split(',')

    def get_company_shareholder(self, fail_silently=False):
        """
        return company shareholder, raise ValueError if not existing
        """
        try:
            return self.shareholder_set.earliest('id')
        except Shareholder.DoesNotExist:
            logger.warning('no company shareholder found')
            if not fail_silently:
                raise ValueError('corp shareholder not found')

    def get_dispo_shareholder(self):
        """
        return shareholder obj which holds all dispo shares (shares which are
        owned by someone but are not registered with the share register under
        his name)
        """
        shareholders = Shareholder.tagged.with_all(
            DISPO_SHAREHOLDER_TAG, self.shareholder_set.all())
        if shareholders.count() > 1:
            raise ValueError('too many dispo shareholders for this company')
        elif shareholders.count() == 1:
            return shareholders[0]

    def get_management_share_count(self, security=None, date=None):
        """ return number of shares owned by management """
        count = 0
        for sh in self.shareholder_set.filter(is_management=True):
            count += sh.share_count(security=security, date=date)
        return count

    def get_management_cumulated_face_value(self, security=None, date=None):
        """ return number of shares owned by management """
        count = 0
        for sh in self.shareholder_set.filter(is_management=True):
            count += sh.cumulated_face_value(security=security, date=date)
        return count

    def get_new_certificate_id(self):
        """
        returns new usable certificate id
        """
        positions = Position.objects.filter(
            Q(buyer__company=self) | Q(seller__company=self),
            certificate_id__isnull=False)
        options = OptionTransaction.objects.filter(
            certificate_id__isnull=False,
            option_plan__company=self)
        positions_cert_ids = positions.values_list('certificate_id', flat=True)
        options_cert_ids = options.values_list('certificate_id', flat=True)
        cert_ids = set(list(positions_cert_ids) + list(options_cert_ids))
        if cert_ids:
            max_cert_id = natsorted(cert_ids)[-1]
            new_cert_id = int(''.join(re.findall(r'\d+', max_cert_id))) + 1
            return new_cert_id
        else:
            return 1

    def get_new_shareholder_number(self):
        """
        returns new usable shareholder number
        """
        qs = self.shareholder_set.all()
        dispo_sh = self.get_dispo_shareholder()
        if dispo_sh:
            qs = qs.exclude(pk=dispo_sh.pk)

        numbers = qs.values_list('number', flat=True)
        if numbers:
            numbers = [''.join(re.findall(r'\d+', n)) for n in numbers]
            max_number = natsorted(numbers, reverse=True)[0]
            new_number = int(max_number) + 1
            return new_number
        else:
            return 1

    def get_logo_url(self):
        """ return url for logo """
        if not self.logo:
            return

        kwargs = {'crop': 'center', 'quality': 99, 'format': "PNG"}
        return get_thumbnail(self.logo.file, 'x80', **kwargs).url

    def get_operators(self):
        return self.operator_set.all().distinct()

    def get_provisioned_capital(self):
        """ its libiertes or eingelegtes capital. means on company
        foundation the capital is provisioned by the shareholders.
        e.g. if company was founded with 1m chf equity, owners might have
        provided only 200k. this value here would then be 200k """

        return self.provisioned_capital

    def get_total_capital(self):
        """ returns the total monetary value of the companies
        capital (Nennkapital) by getting all share creation positions (inital
        and increases) and sum up count*val
        """
        cap_creating_positions = Position.objects.filter(
            buyer__company=self, seller__isnull=True)
        val = 0
        for position in cap_creating_positions:
            face_value = position.security.face_value or 1
            val += position.count * face_value

        cap_destroying_positions = Position.objects.filter(
            seller__company=self, buyer__isnull=True)

        for position in cap_destroying_positions:
            face_value = position.security.face_value or 1
            val -= position.count * face_value

        return val

    def get_total_share_count(self, security=None):
        cap_creating_positions = Position.objects.filter(
            buyer__company=self, seller__isnull=True)
        if security:
            cap_creating_positions = cap_creating_positions.filter(
                security=security)
        val = 0
        for position in cap_creating_positions:
            val += position.count

        cap_destroying_positions = Position.objects.filter(
            seller__company=self, buyer__isnull=True)

        if security:
            cap_destroying_positions = cap_destroying_positions.filter(
                security=security)

        for position in cap_destroying_positions:
            val -= position.count

        return val

    def get_total_share_count_floating(self, security=None):
        """
        how many shares are spread among the outer world/non company shareholder
        """
        total_shares = self.get_total_share_count(security=security)
        company_shareholder_count = self.get_company_shareholder().share_count(
            security=security)
        ds = self.get_dispo_shareholder()
        dispo_shares = ds and self.get_dispo_shareholder().share_count(
                security=security) or 0
        return total_shares - company_shareholder_count - dispo_shares

    def get_total_votes(self, security=None):
        """
        returns the total number of voting rights the company is existing
        """
        votes = 0
        vote_ratio = self.vote_ratio or 1
        qs = [security] if security else self.security_set.all()
        for security in qs:
            face_value = security.face_value or 1
            votes += face_value * security.count / vote_ratio
        return int(votes)

    def get_total_votes_floating(self, security=None):
        """
        returns total amount of votes owned by regular shareholers. excludes
        votes owned by company and non-registered votes
        """
        company_votes = self.get_company_shareholder().vote_count(
            security=security)
        ds = self.get_dispo_shareholder()
        dispo_votes = ds and self.get_dispo_shareholder().vote_count(
                security=security) or 0
        return (self.get_total_votes(security=security) - company_votes -
                dispo_votes)

    def get_total_votes_in_options(self, security=None):
        option_votes = 0
        vote_ratio = self.vote_ratio or 1
        qs = [security] if security else self.security_set.all()
        for security in qs:
            face_value = security.face_value or 1
            option_votes += (self.get_total_options(security=security) *
                             face_value / vote_ratio)
        return option_votes

    def get_total_votes_eligible(self, date=None, security=None):
        """
        returns number of total votes permitted to vote

        math is : total - options - dispo - company
        """
        total = (
            self.get_total_votes_floating(security=security) -
            self.get_total_votes_in_options(security=security)
        )

        return int(total)

    def get_total_options(self, security=None):
        """
        count of shares granted through options
        """
        options_created = OptionTransaction.objects.filter(
            buyer__company=self, seller__isnull=True)

        if security:
            options_created = options_created.filter(
                option_plan__security=security)

        val = 0
        for position in options_created:
            val += position.count

        options_destroyed = OptionTransaction.objects.filter(
            seller__company=self, buyer__isnull=True)

        if security:
            options_destroyed = options_destroyed.filter(
                option_plan__security=security)

        for position in options_destroyed:
            val -= position.count

        return val

    def get_total_options_floating(self):
        """
        count of shares granted through options
        """
        options_created = OptionTransaction.objects.filter(
            buyer__company=self, seller=self.get_company_shareholder())
        val = 0
        for position in options_created:
            val += position.count

        options_returned = OptionTransaction.objects.filter(
            seller__company=self, buyer=self.get_company_shareholder())

        for position in options_returned:
            val -= position.count

        return val

    def get_transfer_shareholder(self):
        """ return shareholder which is tagged as transfer shareholder """
        shareholders = Shareholder.tagged.with_all(
            TRANSFER_SHAREHOLDER_TAG, self.shareholder_set.all())
        if shareholders.count() > 1:
            raise ValueError('too many transfer shareholders for this company')
        elif shareholders.count() == 1:
            return shareholders.first()

    # --- CHECKS
    def has_management(self):
        return self.shareholder_set.filter(is_management=True).exists()

    def has_printed_certificates(self):
        """ returns bool if at least one certificate was printed/has printed
        date
        """
        ots = OptionTransaction.objects.filter(option_plan__company=self,
                                               printed_at__isnull=False
                                               )
        poss = Position.objects.filter(
            Q(buyer__company=self) | Q(seller__company=self),
            printed_at__isnull=False)

        return ots.exists() or poss.exists()

    def has_vested_positions(self):
        """ returns bool if company has at least one position (option/
        transaction) which vesting_months
        """
        return (Position.objects.filter(
            Q(seller__company=self) | Q(buyer__company=self),
            vesting_months__gt=0).exists() or
            OptionTransaction.objects.filter(
                option_plan__company=self,
                vesting_months__gt=0).exists()
            )

    def get_statement_template(self):
        """
        return template for statement pdf (maybe company specific)
        """
        company_template = 'pdf/statement.{}.pdf.html'.format(self.pk)
        fallback_template = 'pdf/statement.pdf.html'  # shareholder/templates
        return select_template([company_template, fallback_template])

    statement_template = property(get_statement_template)

    # --- LOGIC
    def split_shares(self, data):
        """ split all existing positions """
        execute_at = data['execute_at']
        dividend = float(data['dividend'])
        divisor = float(data['divisor'])
        security = data['security']

        # get all active shareholder on day 'execute_at'
        shareholders = self.get_active_shareholders(date=execute_at)
        company_shareholder = self.get_company_shareholder()

        # create return transactions to return old assets to company
        # create transaction to hand out new assets to shareholders with
        # new count
        value = company_shareholder.last_traded_share_price(
            date=execute_at, security=security)
        partials = {}
        for shareholder in shareholders:
            count = shareholder.share_count(
                execute_at, security)
            kwargs1 = {
                'buyer': company_shareholder,
                'seller': shareholder,
                'count': count,
                'value': value,
                'security': security,
                'bought_at': execute_at,
                'is_split': True,
                'comment': _('Share split of {} on {} with ratio {}:{}. '
                             'Return of old shares.').format(
                                 security, execute_at.date(),
                                 int(dividend), int(divisor)),
            }
            if value:
                kwargs1.update({'value': float(value)})
            if shareholder.pk == company_shareholder.pk:
                kwargs1.update(dict(buyer=None, count=self.share_count,
                                    value=shareholder.buyer.first().value))

            p = Position.objects.create(**kwargs1)
            logger.info('Split: share returned {}'.format(p))

            part, count2 = math.modf(count * divisor / dividend)
            kwargs2 = {
                'buyer': shareholder,
                'seller': company_shareholder,
                'count': count2,
                'security': security,
                'bought_at': execute_at,
                'is_split': True,
                'comment': _('Share split of {} on {} with ratio {}:{}. '
                             'Provisioning of new shares.').format(
                                 security, execute_at.date(),
                                 int(dividend), int(divisor)),
            }
            if value:
                kwargs2.update({'value': float(value) / divisor * dividend})
            if shareholder.pk == company_shareholder.pk:
                part, count2 = math.modf(
                    self.share_count /
                    dividend * float(divisor)
                )
                kwargs2.update({
                    'count': count2,
                    'seller': None,
                })

            p = Position.objects.create(**kwargs2)
            if part != 0.0:
                partials.update({shareholder.pk: round(part, 6)})
            logger.info('Split: share issued {}'.format(p))

        # update share count
        self.share_count = int(
            self.share_count / dividend * float(divisor)
        )

        # record partial shares to operator
        self._send_partial_share_rights_email(partials)

        self.save()

    def has_feature_enabled(self, feature_name):
        """
        checks if `feature_name` is available in current subscription
        """

        customer = self.get_customer()
        if not customer.has_active_subscription():
            return False

        feature_list = settings.DJSTRIPE_PLANS.get(
            self.get_current_subscription_plan(), {}).get('features', [])

        return feature_name.lower() in feature_list

    def get_current_subscription_plan(self, display=False):
        """
        return plan name of current subscription (if available)
        """
        customer = self.get_customer()
        if customer.has_active_subscription():
            if display:
                return customer.current_subscription.plan_display()
            return customer.current_subscription.plan

    def get_current_subscription_plan_display(self):
        return self.get_current_subscription_plan(display=True)

    def get_customer(self):
        """
        returns djstripe.Customer object
        """
        customer, created = DjStripeCustomer.get_or_create(subscriber=self)
        return customer

    def validate_plan(self, plan_name, include_errors=True):
        """
        run all validators for company to check if given plan can be subscribed
        if `include_errors` is True, a tuple is returned (bool, error_list)
        """
        plan = settings.DJSTRIPE_PLANS.get(plan_name, {})
        validators = plan.get('validators', [])
        errors = []
        for validator in validators:
            validator_class = import_string(validator)
            try:
                validator_class(self)(plan_name)
            except ValidationError as ex:
                errors.append(ex)

        result = bool(not errors)

        if not include_errors:
            return result

        return (result, errors)

    def can_subscribe_plan(self, plan_name):
        """
        check if company can subscribe to given plan
        """
        return self.validate_plan(plan_name, include_errors=False)

    @property
    def subscription_features(self):
        """
        return list of subscription features for currently subscribed plan
        """
        plan_name = self.get_current_subscription_plan()
        if plan_name:
            return (settings.DJSTRIPE_PLANS.get(plan_name, {})
                    .get('features', {}).keys())
        return []

    # permissions
    def shareholders_count(self):
        return self.shareholder_set.count()

    def securities_count(self):
        return self.security_set.count()

    @property
    def subscription_permissions(self):
        """
        return list of permission that are dependent on subscription features
        """
        permissions = []
        plan_name = self.get_current_subscription_plan()
        plan = settings.DJSTRIPE_PLANS.get(plan_name, {})
        for feature_name, feature_config in plan.get('features', {}).items():
            action_validators = feature_config.get('validators', {})
            for action, validators in action_validators.items():
                action_valid = True
                for validator in validators:
                    validator_class = import_string(validator)
                    try:
                        validator_class(self)()
                    except ValidationError:
                        action_valid = False

                if action_valid:
                    permission_name = '{}_{}'.format(action, feature_name)
                    permissions.append(permission_name)

        return permissions


class UserProfile(AddressModelMixin, models.Model):

    # legal types of a user
    LEGAL_TYPES = (
        ('H', _('Human Being')),
        ('C', _('Corporate')),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL)

    title = models.CharField(max_length=255, blank=True, null=True)
    salutation = models.CharField(max_length=255, blank=True, null=True)

    language = language_fields.LanguageField(blank=True, null=True)
    nationality = models.ForeignKey(Country, blank=True, null=True,
                                    related_name='nationality')
    url = models.URLField(blank=True, null=True)

    legal_type = models.CharField(
        max_length=1, choices=LEGAL_TYPES, default='H',
        help_text=_('legal type of the user'))
    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_department = models.CharField(max_length=255, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    initial_registration_at = models.DateField(
        _('when did the user register with the share register 1st time.'),
        blank=True, null=True)

    ip = models.GenericIPAddressField(blank=True, null=True)
    tnc_accepted = models.BooleanField(default=False)
    is_multi_company_allowed = models.BooleanField(default=False)

    def __unicode__(self):
        return u"%s, %s %s" % (self.city, self.province,
                               str(self.country))

    class Meta:
        verbose_name_plural = "UserProfile"

    def clean(self, *args, **kwargs):
        super(UserProfile, self).clean(*args, **kwargs)

        if self.legal_type == 'C' and not self.company_name:
            raise ValidationError(_('user with legal type company must have '
                                    'company name set'))

        if not self.legal_type == 'C' and self.company_name:
            raise ValidationError(_('user company must have legal type set to '
                                    'company'))

    def get_address(self):
        """ return string with full address """
        fields = ['street', 'street2', 'pobox', 'postal_code', 'city']
        fields = [field for field in fields if getattr(self, field, None)]
        parts = [getattr(self, field) for field in fields]
        address = u", ".join(parts)
        if self.c_o:
            address += u"c/o: {}".format(self.c_o)
        if self.pobox:
            address += u"POBOX: {}".format(self.pobox)
        if self.country:
            address += u", {}".format(self.country.name)
        return address


class Shareholder(TagMixin, models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    company = models.ForeignKey('Company', verbose_name="Shareholders Company")
    number = models.CharField(max_length=255)
    mailing_type = models.CharField(
        _('how should the shareholder be approached by the corp'), max_length=1,
        choices=MAILING_TYPES, blank=True, null=True)
    is_management = models.BooleanField(
        _('user is management/board member of company'), default=False)
    order_cache = JSONField(_('cache data for fast sorting here'),
                            default=dict, blank=True, null=True)

    def __unicode__(self):
        return u'{} {} (#{})'.format(
            self.user.first_name, self.user.last_name, self.number)

    def can_view(self, user):
        """
        permission method to check if user is permitted to view shareholder obj
        """
        # shareholder can see hos own stuff
        if user == self.user:
            return True

        # user is an operator
        if self.company.operator_set.filter(user=user).exists():
            return True

        return False

    def cumulated_face_value(self, security=None, date=None):
        """
        return face value of security * share count
        """
        if security:
            if security.face_value:
                return (self.share_count(security=security, date=date) *
                        security.face_value)
            else:
                return 'n/a'

        # get total
        securities = self.company.security_set.all()
        cface_value = 0
        for sec in securities:
            if sec.face_value:
                cface_value += (self.share_count(security=sec, date=date) *
                                sec.face_value)

        return cface_value

    def current_segments(self, security, date=None):
        """
        returns deflated segments which are owned by this shareholder.
        includes segments blocked for options.
        """
        logger.info('current items: starting')
        date = date or timezone.now()

        # all pos before date
        qs_bought = self.buyer.filter(bought_at__lte=date)
        qs_sold = self.seller.filter(bought_at__lte=date)

        qs_bought = qs_bought.filter(security=security)
        qs_sold = qs_sold.filter(security=security)

        logger.info('current items: qs done')
        # -- flat list of bought items
        segments_bought = qs_bought.values_list(
            'number_segments', flat=True)
        # flatten, unsorted with duplicates
        segments_bought = [
            segment for sublist in segments_bought for segment in sublist]

        # flat list of sold segments
        segments_sold = qs_sold.values_list(
            'number_segments', flat=True)
        segments_sold = [
            segment for sublist in segments_sold for segment in sublist]
        logger.info('current items: flat lists done. inflating...')

        segments_owning = []

        # inflate to have int only
        segments_bought = inflate_segments(segments_bought)
        segments_sold = inflate_segments(segments_sold)
        logger.info('current items: iterating through bought segments...')

        segments_owning = substract_list(segments_bought, segments_sold)
        logger.info('current items: finished')
        return deflate_segments(segments_owning)

    def current_options_segments(self, security, optionplan=None, date=None):
        """
        returns deflated segments which are owned by this shareholder.
        includes segments blocked for options.
        """
        date = date or timezone.now().date()

        if optionplan:
            qs_bought = self.option_buyer.filter(option_plan=optionplan)
            qs_sold = self.option_seller.filter(option_plan=optionplan)

        # all pos before date
        qs_bought = self.option_buyer.filter(bought_at__lte=date)
        qs_sold = self.option_seller.filter(bought_at__lte=date)

        qs_bought = qs_bought.filter(option_plan__security=security)
        qs_sold = qs_sold.filter(option_plan__security=security)

        # -- flat list of bought items
        segments_bought = qs_bought.values_list(
            'number_segments', flat=True)
        # flatten, unsorted with duplicates
        segments_bought = [
            segment for sublist in segments_bought for segment in sublist]

        # flat list of sold segments
        segments_sold = qs_sold.values_list(
            'number_segments', flat=True)
        segments_sold = [
            segment for sublist in segments_sold for segment in sublist]

        segments_owning = []

        # inflate to have int only
        segments_bought = inflate_segments(segments_bought)
        segments_sold = inflate_segments(segments_sold)

        counter_bought = Counter(segments_bought)
        counter_sold = Counter(segments_sold)
        # set as items can occur only once
        segments_owning = set(counter_bought - counter_sold)
        return deflate_segments(segments_owning)

    def get_full_name(self):
        # return first, last, company name
        name = u""
        if self.user.first_name:
            name += self.user.first_name
        if self.user.last_name:
            if name:
                name += u" "
            name += u"{}".format(self.user.last_name)
        if self.user.userprofile.company_name:
            if name:
                name += u" ({})".format(self.user.userprofile.company_name)
            else:
                name += u"{}".format(self.user.userprofile.company_name)

        return name or self.user.email

    def get_number_segments_display(self):
        """
        returns string for date=today and all securities showing number segments
        """
        text = ""
        for security in self.company.security_set.filter(track_numbers=True):
            text += "{}: {} ".format(
                security.get_title_display(),
                human_readable_segments(self.current_segments(security))
            )
        return text

    def get_certificate_ids(self, security):
        """ return id and issue date of all certificates which are valid """
        positions = self.buyer.filter(
            certificate_id__isnull=False,
            certificate_invalidation_position__isnull=True,
        ).values_list('certificate_id', 'bought_at')
        return list(set([(u"{} ({})".format(p[0], p[1])) for p in positions]))

    def get_depot_types(self, security):
        """ return list of depot types used by shareholder for security. used
        in csv export """
        positions = self.buyer.filter(security=security)
        return list(set([p.get_depot_type_display() for p
                         in positions if p.depot_type]))

    def get_stock_book_ids(self, security):
        """ return list of depot types used by shareholder for security. used
        in csv export """
        positions = self.buyer.filter(security=security)
        return list(set([p.stock_book_id for p in positions
                         if p.stock_book_id]))

    def has_vested_shares(self):
        """ does the shareholder hold or did hold in the past any vested
        shares """
        return self.buyer.filter(vesting_months__isnull=False).exists()

    def is_company_shareholder(self):
        """
        returns bool if shareholder is company shareholder
        """
        return self.company.get_company_shareholder() == self

    def is_dispo_shareholder(self):
        """
        returns bool if shareholder is dispo shareholder
        """
        return self.company.get_dispo_shareholder() == self

    def is_transfer_shareholder(self):
        """
        returns bool if shareholder is dispo shareholder
        """
        return self.company.get_transfer_shareholder() == self

    def last_traded_share_price(self, date=None, security=None):
        qs = Position.objects.filter(buyer__company=self.company)
        if date:
            qs = qs.filter(bought_at__lte=date)
        if security:
            qs = qs.filter(security=security)
        if not qs.exists():
            raise ValueError(
                'No Transactions available to calculate recent share price')

        return qs.latest('bought_at').value

    def options_percent(self, date=None):
        """ returns percentage of shares owned compared to corps
        total shares
        FIXME returns wrong values if the company still holds shares
        after capital increase, which are not distributed to shareholders
        company would then have a percentage of itself, although this is
        not relevant for voting rights, etc.
        """
        total = self.company.share_count
        count = sum(self.option_buyer.all().values_list('count', flat=True)) - \
            sum(self.option_seller.all().values_list('count', flat=True))
        if total:
            return "{:.2f}".format(count / float(total) * 100)
        return False

    def options_count(self, date=None, security=None):
        """ total count of shares for shareholder  """
        date = date or timezone.now()
        qs_bought = self.option_buyer.all()
        qs_sold = self.option_seller.all()

        if date:
            qs_bought = self.option_buyer.filter(bought_at__lte=date)
            qs_sold = self.option_seller.filter(bought_at__lte=date)

        if security:
            qs_bought = qs_bought.filter(option_plan__security=security)
            qs_sold = qs_sold.filter(option_plan__security=security)

        count_bought = sum(qs_bought.values_list('count', flat=True))
        count_sold = sum(qs_sold.values_list('count', flat=True))

        return count_bought - count_sold

    def options_value(self, date=None):
        """ calculate the total values of all shares for this shareholder """
        options_count = self.options_count(date=date)
        if options_count == 0:
            return 0

        # last payed price
        if (
            Position.objects.filter(
                buyer__company=self.company, value__isnull=False
            ).exists()
        ):
            position = Position.objects.filter(
                buyer__company=self.company).latest('bought_at')
        else:
            return 0

        return options_count * position.value

    def owns_segments(self, segments, security):
        """
        check if shareholder owns all those segments either as share

        does not check any kind of options. use owns_options_segments for this
        """

        logger.info('checking if {} owns {}'.format(self, segments))

        if isinstance(segments, str):
            segments = string_list_to_json(segments)
            logger.info('converted string to json')

        logger.info('getting current segments...')
        segments_owning = inflate_segments(self.current_segments(
            security=security))
        failed_segments = []

        logger.info('calculating segments not owning...')
        # shareholder does not own this
        failed_segments = substract_list(
            inflate_segments(segments), segments_owning)

        logger.info('check segment ownership done')

        return (len(failed_segments) == 0,
                deflate_segments(failed_segments),
                deflate_segments(segments_owning))

    def owns_options_segments(self, segments, security):
        """
        check if shareholder owns all those segments either as share
        """
        if isinstance(segments, str):
            segments = string_list_to_json(segments)

        segments_owning = inflate_segments(self.current_options_segments(
            security=security))
        failed_segments = []
        for segment in inflate_segments(segments):

            # shareholder does not own this
            if segment not in segments_owning:
                failed_segments.append(segment)

        return (len(failed_segments) == 0,
                deflate_segments(failed_segments),
                deflate_segments(segments_owning))

    def set_dispo_shareholder(self):
        """ mark this shareholder as disposhareholder """
        if (
                self.company.get_dispo_shareholder() and
                self.company.get_dispo_shareholder() != self
        ):
            raise ValueError('disposhareholder already set')

        self.set_tag(DISPO_SHAREHOLDER_TAG)

    def set_transfer_shareholder(self):
        """ mark shareholder as transfer shareholder. this one is used
        when a share register is transfered into this application. in that case
        this shareholder will serve a s selling party for the initial seeding
        of shares to each resp. shareholder
        """
        if (
                self.company.get_transfer_shareholder() and
                self.company.get_transfer_shareholder() != self
        ):
            raise ValueError('transfer shareholder already set')

        self.set_tag(TRANSFER_SHAREHOLDER_TAG)

    def share_percent(self, date=None, security=None):
        """
        returns percentage of shares in the understanding of shares related
        to the total amount of shares existing. not voting rights.
        hence related to free floating capital.
        """
        total = self.company.share_count
        cs = self.company.get_company_shareholder()

        # we use % as voting rights, hence company does not have it
        if self == cs:
            return False

        # this shareholder total count
        count = self.share_count(date=date, security=security)

        # if we have company.share_count set
        # don't count as total what company currently owns = free floating cap
        if total:
            cs_count = cs.share_count(date=date, security=security)
            # we have no other shareholders
            if total == cs_count:
                return "{:.2f}".format(float(0))

            # do the math
            return "{:.2f}".format(
                count / float(total-cs_count) * 100)

        return False

    def share_count(self, date=None, security=None, only_sellable=False,
                    expired_vesting=False, without_vesting=False):
        """ total count of shares for shareholder. `date` is the date on which
        the shares should be counted for `security` or all securities.
        `only_sellable` excludes shares within the certificate depot.
        `expired_vesting` gets the count for all shares with vesting_months
        but where the vesting period is over. `without_vesting` gets
        share count for all pkgds which don't have a vesting at all
        """

        qs_bought = self.buyer.all()
        qs_sold = self.seller.all()

        if without_vesting:
            # vesting applied to this shareholder is only applied in buyer
            # data, seller data is new vesting data for the buyer
            qs_bought = self.buyer.filter(vesting_months__isnull=True)

        if only_sellable:
            # if there are certificates without invalidation (means still
            # stored at certificate depot, on `only_sellable` request
            # these cannot be counted as possessed shares
            # scenario 1: exclude if it has a cert id and was not invalidated
            # scenario 2: include if it has a cert id and was invalidated
            # -> hide these positions which are neither invalidated
            # nor being the invalidation position to another one
            query = Q(certificate_id__isnull=False,
                      certificate_invalidation_position__isnull=True,
                      certificate_initial_position__isnull=True)
            qs_bought = qs_bought.exclude(query)

        if date:
            qs_bought = qs_bought.filter(bought_at__lte=date)
            qs_sold = qs_sold.filter(bought_at__lte=date)

        if security:
            qs_bought = qs_bought.filter(security=security)
            qs_sold = qs_sold.filter(security=security)

        if expired_vesting:
            # for each buyer position with vesting_months applied, we need to
            # check if the vesting was expired. placed at the end of method
            # because it's a very expensive method and we might have excluded
            # all options till now already
            pks = []
            now = timezone.now()
            for pos in qs_bought:
                if pos.vesting_months:
                    expires_at = pos.bought_at + relativedelta(
                        months=pos.vesting_months)
                    if expires_at <= now.date():
                        pks.append(pos.pk)
                else:
                    pks.append(pos.pk)
            qs_bought = self.buyer.filter(pk__in=pks)

        count_bought = sum(qs_bought.values_list('count', flat=True))
        count_sold = sum(qs_sold.values_list('count', flat=True))

        # clean company shareholder count by options count
        if self.is_company_shareholder():
            options_created = self.company.get_total_options(security=security)
        else:
            options_created = 0

        return count_bought - count_sold - options_created

    def share_count_sellable(self, date=None, security=None):
        """
        returns number of shares for this security on this date which
        are truely sellable. e.g. shares owned but enlisted in
        certificate depot are not sellable

        also excludes vested shares
        """
        # we can skip this expensive code if vestig does not apply:
        if not self.has_vested_shares():
            return self.share_count(date, security, only_sellable=True)

        return self.share_count(date, security, only_sellable=True,
                                expired_vesting=True)

    def share_value(self, date=None):
        """ calculate the total values of all shares for this shareholder """
        share_count = self.share_count(date=date)
        if share_count == 0:
            return 0

        # last payed price
        position = Position.objects.filter(
            buyer__company=self.company,
            value__gt=0
        ).order_by('-bought_at', '-id').first()
        if position:
            return share_count * position.value
        else:
            return 0

    def validate_gafi(self):
        """ returns dict with indication if all data is correct to match
        swiss fatf gafi regulations """
        result = {"is_valid": True, "errors": []}

        # applies only for swiss corps
        if (
            not self.company.country or
            self.company.country.iso_code.lower() != 'ch'
        ):
            return result

        # missing profile leads to global warning
        if not hasattr(self.user, 'userprofile'):
            result['is_valid'] = False
            result['errors'].append(_("Missing all data required for #GAFI."))
            return result

        # humans need names
        legal_type_string = self.user.userprofile.legal_type
        user = self.user

        if (legal_type_string == 'H' and not user.first_name or not
                user.last_name):
            result['is_valid'] = False
            result['errors'].append(_(
                'Shareholder first name or last name missing.'))

        company_name = self.user.userprofile.company_name

        if (legal_type_string == 'C' and not company_name):
            result['is_valid'] = False
            result['errors'].append(_(
                'Company name or last name missing.'))

        if not self.user.userprofile.birthday:
            result['is_valid'] = False
            result['errors'].append(_('Shareholder birthday missing.'))

        if not self.user.userprofile.country:
            result['is_valid'] = False
            result['errors'].append(_('Shareholder origin/country missing.'))

        if (
            not self.user.userprofile.city or
            not self.user.userprofile.postal_code or
            not self.user.userprofile.street
        ):
            result['is_valid'] = False
            result['errors'].append(_(
                'Shareholder address or address details missing.'))

        return result

    def vote_count(self, date=None, security=None):
        """
        returns the total number of voting rights for this shareholder
        """
        votes = 0
        vote_ratio = self.company.vote_ratio or 1
        qs = [security] if security else self.company.security_set.all()
        for security in qs:
            face_value = security.face_value or 1
            votes += (self.share_count(security=security, date=date) *
                      face_value / vote_ratio)
        return int(votes)

    def vote_percent(self, date=None, security=None):
        """
        returns percentage of the users voting rights compared to total voting
        rights existing
        """
        if (self.is_company_shareholder() or
                not self.company.get_total_votes_floating()):
            return float(0.0)

        # do the math
        total_votes_eligible = self.company.get_total_votes_eligible()

        # no floating cap yet, hence cannot continue the math
        if total_votes_eligible == 0:
            return None

        # how much percent of these eligible votes does the shareholder have?
        return (self.vote_count(date=date, security=security) /
                float(total_votes_eligible))


class Operator(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    company = models.ForeignKey('Company', verbose_name="Operators Company")
    share_count = models.PositiveIntegerField(blank=True, null=True)
    last_active_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['company__name']

    def __unicode__(self):
        return u"{} {} ({})".format(
            self.user.first_name, self.user.last_name, self.user.email)


class Security(models.Model):
    SECURITY_TITLES = (
        ('P', _('Preferred Stock')),
        ('C', _('Common Stock')),
        ('R', _('Registered Shares')),
        ('V', _('Registered share with restricted transferability')),
        # ('O', 'Option'),
        # ('W', 'Warrant'),
        # ('V', 'Convertible Instrument'),
    )
    title = models.CharField(max_length=1, choices=SECURITY_TITLES, default='C')
    face_value = models.DecimalField(
        _('Nominal value of this asset'),
        max_digits=16, decimal_places=4, blank=True,
        null=True)
    company = models.ForeignKey(Company)
    count = models.PositiveIntegerField()
    number_segments = JSONField(
        _('JSON list of segments of ids for securities. can be 1, 2, 3, 4-10'),
        default=list)
    cusip = models.CharField(
        _('public security id aka Valor, WKN, CUSIP: http://bit.ly/2ieXwuK'),
        max_length=255, blank=True, null=True)

    # settings
    track_numbers = models.BooleanField(
        _('App needs to track IDs of shares. WARNING: update initial '
          'transaction with segments on enabling.'), default=False)

    class Meta:
        ordering = ['face_value']

    def __unicode__(self):
        if self.face_value:
            return _(u"{} ({} CHF)").format(
                self.get_title_display(), int(self.face_value))

        return self.get_title_display()

    def calculate_count(self):
        """
        calculate how many shares does the company have by iterating
        over all shareholders of the company and getting their
        share count. summarize it.
        """
        return self.company.get_total_share_count(security=self)

    def calculate_dispo_share_count(self):
        """
        caculates the number of shares which are not registered within the share
        register for this security
        """
        total_shares = self.calculate_count()
        floating_shares = self.company.get_total_share_count_floating(
            security=self)
        # options = self.company.get_total_options(security=self)

        return total_shares - floating_shares

    def count_in_segments(self, segments=None):
        """
        returns number of shares contained in segments
        """
        if not segments:
            segments = self.number_segments

        if isinstance(segments, str) or isinstance(segments, unicode):
            segments = string_list_to_json(segments)

        count = 0
        for segment in segments:
            if isinstance(segment, int):
                count += 1
            else:
                start, end = segment.split('-')
                # 3-5 means 3,4,5 means 3 shares
                delta = int(end) - int(start) + 1
                count += delta

        return count

    def get_isin(self):

        if self.cusip:
            return 'CH0{}1'.format(self.cusip)

        return ''


class Position(DiscountedTaxByVestingModelMixin, CertificateMixin):
    """
    aka Transaction
    """

    buyer = models.ForeignKey(
        'Shareholder', related_name="buyer", blank=True, null=True)
    seller = models.ForeignKey('Shareholder', blank=True, null=True,
                               related_name="seller")
    security = models.ForeignKey(Security)
    count = models.PositiveIntegerField(_('Share Count transfered or created'))
    bought_at = models.DateField()
    # needs at least 4 post comma digits to be precise (finanzial math standard)
    value = models.DecimalField(
        _('Nominal value or payed price for the transaction'),
        max_digits=16, decimal_places=4, blank=True,
        null=True)
    is_split = models.BooleanField(
        _('Position is part of a split transaction'), default=False)
    is_draft = models.BooleanField(default=True)
    number_segments = JSONField(
        _('JSON list of segments of ids for securities. can be 1, 2, 3, 4-10'),
        default=list, blank=True, null=True)
    registration_type = models.CharField(
        _('Securities are purchase type (for myself, etc.)'), max_length=1,
        choices=REGISTRATION_TYPES, blank=True, null=True)
    stock_book_id = models.CharField(
        _('aka Skontro (read http://bit.ly/2iJquEl)'),
        max_length=255, blank=True, null=True)
    depot_type = models.CharField(
        _('What kind of depot is this position stored within'), max_length=1,
        choices=DEPOT_TYPES, blank=True, null=True)
    depot_bank = models.ForeignKey(Bank, blank=True, null=True)
    certificate_invalidation_position = models.OneToOneField(
        'self',
        help_text=_('assigned position represents the change back to company '
                    'depot from cert depot'),
        null=True, blank=True, related_name='certificate_initial_position')
    vesting_months = models.PositiveIntegerField(blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"Pos {}->#{}@{}->{}".format(
            self.seller,
            self.count,
            self.value,
            self.buyer
        )

    def can_view(self, user):
        """
        permission method to check if user is permitted to view obj
        """
        if self.buyer and user == self.buyer.user:
            return True
        elif self.seller and user == self.seller.user:
            return True

        # user is an operator
        if self.buyer.company.operator_set.filter(user=user).exists():
            return True

        return False

    def get_position_type(self):
        if not self.seller:
            return _('Capital Increase')
        if self.is_split:
            return _('Part of Split')
        if self.seller.is_company_shareholder():
            if not self.certificate_id:
                return _('Share issue')
            else:
                return _('share issue into cert depot')
        if self.certificate_id and not getattr(
                self, 'certificate_initial_position', None):
            return _('move stock to certificate depot')
        if hasattr(self, 'certificate_initial_position'):
            return _('stock returns from certificate depot')
        return _('Regular Ownership change')

    def get_total_face_value(self):
        """
        returns total of face value times count
        """
        if self.security.face_value:
            return self.count * self.security.face_value

    def invalidate_certificate(self):
        """
        create child position to mark certificate id as invaldidated and the
        depot type to be changed.
        """
        if not Position.objects.filter(
                certificate_invalidation_position=self).exists():
            from copy import deepcopy
            invalidation_position = deepcopy(self)
            invalidation_position.pk = None  # create new obj
            invalidation_position.buyer = self.buyer
            invalidation_position.seller = self.buyer
            invalidation_position.comment = _('Certificate Invalidation for '
                                              'position {}').format(self.pk)
            invalidation_position.bought_at = timezone.now()
            invalidation_position.depot_type = DEPOT_TYPES[1][0]
            invalidation_position.printed_at = None
            invalidation_position.save()
            self.certificate_invalidation_position = invalidation_position
            self.save()
        else:
            raise ValueError('position already invalidated')


def get_option_plan_upload_path(instance, filename):
    return os.path.join(
        "private", "optionplan", "%d" % instance.id, filename)


class OptionPlan(models.Model):
    """ Approved chunk of option (approved by board) """
    company = models.ForeignKey('Company')
    board_approved_at = models.DateField()
    title = models.CharField(max_length=255)
    security = models.ForeignKey('Security')
    exercise_price = models.DecimalField(
        max_digits=8, decimal_places=4,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal('0.01'))]
        )
    count = models.PositiveIntegerField(
        help_text=_("Number of shares approved"))
    comment = models.TextField(blank=True, null=True)
    pdf_file = models.FileField(
        blank=True, null=True,
        upload_to=get_option_plan_upload_path,)
    number_segments = JSONField(
        _('JSON list of segments of ids for securities. can be 1, 2, 3, 4-10'),
        default=list, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"{}".format(self.title)

    def can_view(self, user):
        """
        permission method to check if user is permitted to view obj
        """
        # user is an operator
        if self.company.operator_set.filter(user=user).exists():
            return True

        return False

    def generate_pdf_file_preview(self):
        """ generates preview png in same place """
        from wand.image import Image
        # Converting first page into JPG
        with Image(filename=self.pdf_file.file.name+"[0]") as img:
            width, height = img.size
            # img.resize(300, int(300/float(width)*float(height)))
            img.save(filename=self.pdf_file_preview_path())

    def pdf_file_preview_path(self):
        if not self.pdf_file:
            return None
        s = self.pdf_file.file.name.split(".")
        s = s[:-1]
        s.extend(['png'])
        return ".".join(s)

    def pdf_file_preview_url(self):
        if not self.pdf_file:
            return None
        # needs timestamp to trigger reload
        return "/optionsplan/{}/download/img/?t={}".format(
            self.pk, time.time())

    def pdf_file_url(self):
        if not self.pdf_file:
            return None
        return "/optionsplan/{}/download/pdf/".format(self.pk)


class OptionTransaction(DiscountedTaxByVestingModelMixin, CertificateMixin):
    """ Transfer of options from someone to anyone """
    bought_at = models.DateField()
    buyer = models.ForeignKey('Shareholder', related_name="option_buyer")
    option_plan = models.ForeignKey('OptionPlan')
    count = models.PositiveIntegerField()
    seller = models.ForeignKey('Shareholder', blank=True, null=True,
                               related_name="option_seller")
    vesting_months = models.PositiveIntegerField(blank=True, null=True)
    number_segments = JSONField(
        _('JSON list of segments of ids for securities. can be 1, 2, 3, 4-10'),
        default=list, blank=True, null=True)
    registration_type = models.CharField(
        _('Securities are purchase type (for myself, etc.)'), max_length=1,
        choices=REGISTRATION_TYPES, blank=True, null=True)
    stock_book_id = models.CharField(
        _('aka Skontro (read http://bit.ly/2iJquEl)'),
        max_length=255, blank=True, null=True)
    depot_type = models.CharField(
        _('What kind of depot is this position stored within'), max_length=1,
        choices=DEPOT_TYPES, blank=True, null=True)
    is_draft = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"OpTr {}->#{}->{} (OP:{})".format(
            self.seller,
            self.count,
            self.buyer,
            self.option_plan
        )

    def can_view(self, user):
        """
        permission method to check if user is permitted to view obj
        """
        if (
                user == self.buyer.user or
                (self.seller and user == self.seller.user)
        ):
            return True

        # user is an operator
        if self.buyer.company.operator_set.filter(user=user).exists():
            return True

        return False

    def get_total_face_value(self):
        return self.count * self.option_plan.security.face_value


class ShareholderStatementReport(models.Model):
    """
    report for company regarding all shareholder statements
    """
    company = models.ForeignKey('Company', verbose_name=_('company'))
    report_date = models.DateField(_('report date'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # file including all statements for easy download
    pdf_file = models.FilePathField(path=settings.SHAREHOLDER_STATEMENT_ROOT,
                                    match='.+\.pdf', recursive=True,
                                    max_length=500, null=True, blank=True)

    SIGNING_SALT = 'shareholder.shareholderstatementreport.pdf_download'

    class Meta:
        verbose_name = _('shareholder statement report')
        verbose_name_plural = _('shareholder statement reports')

    def __unicode__(self):  # pragma: nocover
        return u'{} - {}'.format(self.company, date_format(self.report_date))

    def get_pdf_download_url(self, absolute=True):
        """
        return url to download pdf file

        Keyword arguments:
        absolute -- get absolute url including domain (default: True)
        with_auth_token -- append authentication token (default: False)
        """
        if not self.pdf_file:
            return

        url = reverse('all_statements_download_pdf')
        signing_data = dict(
            pk=self.pk,
            company_pk=self.company_id,
            date=str(self.report_date)
        )
        file_hash = signing.dumps(signing_data, salt=self.SIGNING_SALT)
        url += u'?file={}'.format(file_hash)
        if absolute:
            url = u'{}://{}{}'.format(
                (getattr(settings, 'FORCE_SECURE_CONNECTION',
                         not settings.DEBUG) and 'https' or 'http'),
                Site.objects.get_current().domain, url)
        return url

    pdf_download_url = property(get_pdf_download_url)

    def get_statement_count(self):
        """
        get count of all related ShareholderStatements
        """
        return self.shareholderstatement_set.count()

    statement_count = property(get_statement_count)

    def get_pdf_file_size(self, human_readable=True):
        if not self.pdf_file:
            return 0

        if human_readable:
            return human_readable_file_size(os.path.getsize(self.pdf_file))

        return os.path.getsize(self.pdf_file)

    def get_statement_sent_count(self):
        """
        get count of all related ShareholderStatements with email_sent_at set
        """
        return self.shareholderstatement_set.exclude(
            email_sent_at__exact=None).count()

    statement_sent_count = property(get_statement_sent_count)

    def get_statement_letter_count(self):
        """
        get count of all related ShareholderStatements with letter_sent_at set
        """
        return self.shareholderstatement_set.exclude(
            letter_sent_at__exact=None).count()

    statement_letter_count = property(get_statement_letter_count)

    def get_statement_opened_count(self):
        """
        get count of all related ShareholderStatements with email_opened_at set
        """
        return self.shareholderstatement_set.exclude(
            email_opened_at__exact=None).count()

    statement_opened_count = property(get_statement_opened_count)

    def get_statement_downloaded_count(self):
        """
        get count of all related ShareholderStatements with pdf_downloaded_at
        set
        """
        return self.shareholderstatement_set.exclude(
            pdf_downloaded_at__exact=None).count()

    statement_downloaded_count = property(get_statement_downloaded_count)

    def generate_statements(self, send_notify=True):
        """
        generate statements for shareholder users of company,
        then set the statement_sending_date on company to next year
        """

        # check company subscription
        if not self.company.has_feature_enabled('shareholder_statements'):
            return

        corp_shareholders = [
            self.company.get_company_shareholder(fail_silently=True),
            self.company.get_dispo_shareholder(),
            self.company.get_transfer_shareholder()
        ]
        corp_shareholders = [sh.pk for sh in corp_shareholders if sh]
        shareholders = self.company.shareholder_set.exclude(
            pk__in=corp_shareholders)
        users = get_user_model().objects.filter(
            pk__in=shareholders.values_list('user_id', flat=True))
        for user in users:
            statement, created = self._create_shareholder_statement_for_user(
                user)
            if created and send_notify:
                statement.send_email_notification()

        self._create_joint_statements_pdf()

        # set new sending date
        if self.company.statement_sending_date:
            self.company.statement_sending_date += relativedelta(
                year=self.company.statement_sending_date.year + 1)
            self.company.save()

    def _create_joint_statements_pdf(self):
        """ merge all statement pdf files into a big single one for download """
        pdf_filepath = self._get_statement_pdf_path_for_joint_pdf()
        # merge
        count = int(math.ceil(
            self.shareholderstatement_set.all().count() / 100))
        # merge in chunks to avoid "Too many files open"
        partials = []
        for x in range(1, count):
            partial_filepath = pdf_filepath + '-{}'.format(x)
            qs = self.shareholderstatement_set.all()[(x-1)*100:x*100]
            pdf_file_paths = [statement.pdf_file for statement in
                              qs if statement.pdf_file]
            merge_pdf(pdf_file_paths, partial_filepath)
            partials.append(partial_filepath)

        merge_pdf(partials, pdf_filepath)
        for f in partials:  # remove partials
            os.remove(f)

        # save to model
        self.pdf_file = pdf_filepath
        self.save()

    def _get_statement_pdf_path_for_joint_pdf(self):
        # prepare path and filename
        path = os.path.join(settings.SHAREHOLDER_STATEMENT_ROOT,
                            'allinone',
                            str(self.company_id),
                            str(self.report_date.year))
        if not os.path.exists(path):
            os.makedirs(path)
        pdf_filename = u'all-statements-{}-{}.pdf'.format(
            slugify(self.company),
            self.report_date.strftime('%Y-%m-%d')
        )
        pdf_filepath = os.path.join(path, pdf_filename)
        return pdf_filepath

    def _get_statement_pdf_path_for_user(self, user):
        """
        returns a unique directory path to for the user
        """
        path = os.path.join(settings.SHAREHOLDER_STATEMENT_ROOT,
                            str(user.pk),
                            str(self.company_id),
                            str(self.report_date.year))
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def _create_shareholder_statement_for_user(self, user):
        """
        create the shareholder statement for all shareholders of self.company
        for given user
        """

        statement, created = None, False

        # check if user has shareholder(s)
        user_shareholders = user.shareholder_set.all()
        if not user_shareholders.count():
            return (None, False)

        # check if shareholder/user has any shares or options
        share_count = sum([s.share_count(date=self.report_date)
                           for s in user_shareholders])
        options_count = sum([s.options_count(date=self.report_date)
                             for s in user_shareholders])

        if not sum([share_count, options_count]):
            # nothing for a statement
            return (statement, created)

        if self.shareholderstatement_set.filter(user=user).exists():
            # FIXME: what to do? for now we don't change any existing entries
            statement = self.shareholderstatement_set.filter(user=user).get()

        pdf_dir = self._get_statement_pdf_path_for_user(user)
        pdf_filename = u'{}-{}-{}.pdf'.format(
            slugify(user.shareholder_set.first().get_full_name()),
            slugify(self.company),
            self.report_date.strftime('%Y-%m-%d')
        )
        pdf_filepath = os.path.join(pdf_dir, pdf_filename)

        if not statement or not os.path.isfile(statement.pdf_file):

            # create pdf
            context = dict(
                report=self,
                company=self.company,
                report_date=self.report_date,
                user=user,
                user_name=user.shareholder_set.first().get_full_name(),
                shareholder_list=self.company.shareholder_set.filter(
                    user_id=user.pk),
                site=Site.objects.get_current(),
                STATIC_URL=settings.STATIC_URL,
                MEDIA_ROOT=settings.STATIC_ROOT,
            )

            if not self._create_statement_pdf(pdf_filepath, context):
                # TODO: handle error properly
                raise Exception('Error generating statement pdf')

            if not statement:
                statement = self.shareholderstatement_set.create(
                    user=user, pdf_file=pdf_filepath)
                created = True
            else:
                statement.pdf_file = pdf_filepath
                statement.save()

        return (statement, created)

    def _create_statement_pdf(self, filepath, context):
        """
        generate pdf file of statement
        """
        activate_lang(settings.LANGUAGE_CODE)
        # check for a custom company template
        try:
            pdf = render_pdf(self.company.statement_template.render(context))
        except Exception as e:
            logger.exception('Error generating statement pdf', extra={'ex': e})
            return False

        with open(filepath, 'w') as f:
            f.write(pdf)

        return True


class ShareholderStatement(models.Model):
    """
    statement with snapshot of data of all shareholders of the user
    """
    report = models.ForeignKey(ShareholderStatementReport,
                               verbose_name=_('shareholder statement report'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    pdf_file = models.FilePathField(path=settings.SHAREHOLDER_STATEMENT_ROOT,
                                    match='.+\.pdf', recursive=True,
                                    max_length=500)

    # metrics
    email_sent_at = models.DateTimeField(_('email sent at'),
                                         null=True, blank=True)
    email_opened_at = models.DateTimeField(_('email opened at'),
                                           null=True, blank=True)
    pdf_downloaded_at = models.DateTimeField(_('PDF downloaded at'),
                                             null=True, blank=True)
    letter_sent_at = models.DateTimeField(_('letter sent at'),
                                          null=True, blank=True)

    remote_email_id = models.CharField(
        _('remote email id'), max_length=200, blank=True,
        validators=[validate_remote_email_id],
        help_text=_(
            'Prefix id with provider, e.g. mandrill{sep}[EMAIL_ID]').format(
            **dict(sep=getattr(settings, 'REMOTE_EMAIL_SEPARATOR', '$')))
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    SIGNING_SALT = 'shareholder.shareholderstatement.pdf_download'

    class Meta:
        verbose_name = _('shareholder statement')
        verbose_name_plural = _('shareholder statements')
        unique_together = ('report', 'user')

    def __unicode__(self):  # pragma: nocover
        return u'{}: {}'.format(self.user, self.report)

    def send_email_notification(self):
        """
        send a notification to the user
        """
        from .tasks import send_statement_email

        if not self.user.email:
            # sent letter immediately
            self.send_letter()
        else:
            # call task
            send_statement_email.delay(self.pk)

    def send_letter(self):
        """
        send letter with statement PDF to user
        """
        from .tasks import send_statement_letter
        # call task
        send_statement_letter.delay(self.pk)

    def get_pdf_download_url(self, absolute=True, with_auth_token=False):
        """
        return url to download pdf file

        Keyword arguments:
        absolute -- get absolute url including domain (default: True)
        with_auth_token -- append authentication token (default: False)
        """
        if not self.pdf_file:
            return

        url = reverse('statement_download_pdf')
        signing_data = dict(
            pk=self.pk,
            user_pk=self.user_id,
            company_pk=self.report.company_id,
            date=str(self.report.report_date)
        )
        file_hash = signing.dumps(signing_data, salt=self.SIGNING_SALT)
        url += u'?file={}'.format(file_hash)
        if with_auth_token:
            url += u'&token={}'.format(self.user.auth_token.key)
        if absolute:
            url = u'{}://{}{}'.format(
                (getattr(settings, 'FORCE_SECURE_CONNECTION',
                         not settings.DEBUG) and 'https' or 'http'),
                Site.objects.get_current().domain, url)
        return url

    pdf_download_url = property(get_pdf_download_url)


# --------- DJANGO TAGGING ----------
register(Shareholder)


# --------- SIGNALS ----------
# must be inside a file which is imported by django on startup
# @jirsch: use apps.py for signal registration!
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """ create rest API access token and user profile obj on
    User obj create """

    if created:
        Token.objects.create(user=instance)
        profile = getattr(instance, 'userprofile',
                          UserProfile.objects.create(user=instance))
        if instance.first_name == settings.COMPANY_INITIAL_FIRST_NAME:
            profile.legal_type = 'C'
            profile.save()


@receiver(post_save, sender=settings.DJSTRIPE_SUBSCRIBER_MODEL)
def create_stripe_customer(sender, instance=None, created=False, **kwargs):
    """create stripe customer object when subscriber is created"""
    enabled = getattr(
        settings, 'CREATE_STRIPE_CUSTOMER_FOR_SUBSCRIBER_ON_CREATE', True)
    if enabled and created:
        instance.get_customer()
