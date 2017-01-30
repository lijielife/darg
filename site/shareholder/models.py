import datetime
import logging
import math
import os
import time
from collections import Counter
from decimal import Decimal

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.core.mail import send_mail
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext as _
from django_languages import fields as language_fields
from rest_framework.authtoken.models import Token
from sorl.thumbnail import get_thumbnail
from tagging.registry import register
from tagging.models import Tag

from shareholder.validators import ShareRegisterValidator
from utils.formatters import (deflate_segments, flatten_list,
                              human_readable_segments, inflate_segments,
                              string_list_to_json)
from utils.math import substract_list


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

logger = logging.getLogger(__name__)


class TagMixin(object):
    """
    mixin to make tagging objects available inside models
    """
    def set_tag(self, tag):
        Tag.objects.update_tags(self, tag)

    def get_tags(self):
        return Tag.objects.get_for_object(self)


class Country(models.Model):
    """Model for countries"""
    iso_code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=45, blank=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ["name", "iso_code"]


def get_company_logo_upload_path(instance, filename):
    return os.path.join(
        "public", "company", "%d" % instance.id, "logo", filename)


class Company(models.Model):

    name = models.CharField(max_length=255)
    share_count = models.PositiveIntegerField(blank=True, null=True)
    country = models.ForeignKey(
        Country, null=True, blank=False, help_text=_("Headquarter location"))
    founded_at = models.DateField(
        _('Foundation date of the company'),
        null=True, blank=False)
    provisioned_capital = models.PositiveIntegerField(blank=True, null=True)
    logo = models.ImageField(
        blank=True, null=True,
        upload_to=get_company_logo_upload_path,)
    vote_ratio = models.PositiveIntegerField(
        _('Voting rights calculation: one vote per X of security.face_value'),
        blank=True, null=True, default=1)

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

    def get_active_shareholders(self, date=None):
        """ returns list of all active shareholders """
        shareholder_list = []
        for shareholder in self.shareholder_set.all().order_by('number'):
            if shareholder.share_count(date=date) > 0:
                shareholder_list.append(shareholder.pk)

        return Shareholder.objects.filter(
            pk__in=shareholder_list
        ).select_related(
            'user', 'user__userprofile', 'user__userprofile__country', 'company'
        ).order_by('number')

    def get_active_option_holders(self, date=None):
        """ returns list of all active shareholders """
        oh_list = []
        # get all users
        sh_ids = self.optionplan_set.all().filter(
            optiontransaction__isnull=False
            ).values_list(
            'optiontransaction__buyer__id', flat=True).distinct()
        for sh_id in sh_ids:
            sh = Shareholder.objects.get(id=sh_id)
            bought_options = sh.option_buyer.aggregate(Sum('count'))
            sold_options = sh.option_seller.aggregate(Sum('count'))
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

    def get_company_shareholder(self):
        """
        return company shareholder, raise ValueError if not existing
        """
        try:
            return self.shareholder_set.earliest('id')
        except Shareholder.DoesNotExist:
            raise ValueError('Company Shareholder does not exist')

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
        return total_shares - company_shareholder_count

    def get_total_votes(self, security=None):
        """
        returns the total number of voting rights the company is existing
        """
        votes = 0
        qs = [security] if security else self.security_set.all()
        for security in qs:
            face_value = security.face_value or 1
            ratio = self.vote_ratio or 1
            votes += face_value * security.count / ratio

        return int(votes)

    def get_total_votes_floating(self, security=None):
        """
        returns total amount of votes owned by regular shareholers. excludes
        votes owned by company and options
        """
        company_votes = self.get_company_shareholder().vote_count(
            security=security)
        return self.get_total_votes(security=security) - company_votes

    def get_total_votes_in_options(self, security=None):
        qs = self.security_set.all()
        ratio = self.vote_ratio or 1

        if security:
            qs = [security]

        option_votes = 0
        for security in qs:
            face_value = security.face_value or 1
            option_votes += (self.get_total_options(security=security) *
                             face_value / ratio)

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

        # if we have a dispo shareholder, substract his votes too...
        dsh = self.get_dispo_shareholder()
        if dsh:
            total = total - dsh.vote_count(date=date, security=security)

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

    def get_logo_url(self):
        """ return url for logo """
        if not self.logo:
            return

        kwargs = {'crop': 'center', 'quality': 99, 'format': "PNG"}
        return get_thumbnail(self.logo.file, 'x40', **kwargs).url

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


class UserProfile(models.Model):

    # legal types of a user
    LEGAL_TYPES = (
        ('H', _('Human Being')),
        ('C', _('Corporate')),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=255, blank=True, null=True)
    salutation = models.CharField(max_length=255, blank=True, null=True)

    street = models.CharField(max_length=255, blank=True, null=True)
    street2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    pobox = models.CharField(max_length=255, blank=True, null=True)
    c_o = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=255, blank=True, null=True)
    country = models.ForeignKey(Country, blank=True, null=True)
    language = language_fields.LanguageField(blank=True, null=True)
    nationality = models.ForeignKey(Country, blank=True, null=True,
                                    related_name='nationality')

    legal_type = models.CharField(
        max_length=1, choices=LEGAL_TYPES, default='H',
        help_text=_('legal type of the user'))
    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_department = models.CharField(max_length=255, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)

    ip = models.GenericIPAddressField(blank=True, null=True)
    tnc_accepted = models.BooleanField(default=False)

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


class Shareholder(TagMixin, models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    company = models.ForeignKey('Company', verbose_name="Shareholders Company")
    number = models.CharField(max_length=255)
    mailing_type = models.CharField(
        _('how should the shareholder be approached by the corp'), max_length=1,
        choices=MAILING_TYPES, blank=True, null=True)

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

        return name

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

    def set_dispo_shareholder(self):
        """ mark this shareholder as disposhareholder """
        if (
                self.company.get_dispo_shareholder() and
                self.company.get_dispo_shareholder() != self
        ):
            raise ValueError('disposhareholder already set')

        self.set_tag(DISPO_SHAREHOLDER_TAG)

    def share_percent(self, date=None):
        """
        returns percentage of shares in the understanding of voting rights.
        hence related to free floating capital.
        """
        total = self.company.share_count
        cs = self.company.get_company_shareholder()

        # we use % as voting rights, hence company does not have it
        if self == cs:
            return False

        # this shareholder total count
        count = sum(self.buyer.all().values_list('count', flat=True)) - \
            sum(self.seller.all().values_list('count', flat=True))

        # id we have company.share_count set
        # don't count as total what company currently owns = free floating cap
        if total:

            # we have no other shareholders
            if total == cs.share_count(date):
                return "{:.2f}".format(float(0))

            # do the math
            return "{:.2f}".format(
                count / float(total-cs.share_count(date)) * 100)

        return False

    def share_count(self, date=None, security=None):
        """ total count of shares for shareholder  """
        qs_bought = self.buyer.all()
        qs_sold = self.seller.all()

        if date:
            qs_bought = self.buyer.filter(bought_at__lte=date)
            qs_sold = self.seller.filter(bought_at__lte=date)

        if security:
            qs_bought = qs_bought.filter(security=security)
            qs_sold = qs_sold.filter(security=security)

        count_bought = sum(qs_bought.values_list('count', flat=True))
        count_sold = sum(qs_sold.values_list('count', flat=True))

        # clean company shareholder count by options count
        if self.is_company_shareholder():
            options_created = self.company.get_total_options(security=security)
        else:
            options_created = 0

        return count_bought - count_sold - options_created

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

        if not (self.user.first_name and self.user.last_name) or not \
                self.user.userprofile.company_name:
            result['is_valid'] = False
            result['errors'].append(_(
                'Shareholder first name, last name or company name missing.'))

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
        date = date or datetime.datetime.now()
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

    def current_segments(self, security, date=None):
        """
        returns deflated segments which are owned by this shareholder.
        includes segments blocked for options.
        """
        logger.info('current items: starting')
        date = date or datetime.datetime.now()

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
        date = date or datetime.datetime.now().date()

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

    def vote_count(self, date=None, security=None):
        """
        returns the total number of voting rights for this shareholder
        """
        votes = 0
        ratio = self.company.vote_ratio or 1
        qs = [security] if security else self.company.security_set.all()
        for security in qs:
            face_value = security.face_value or 1
            votes += (self.share_count(security=security, date=date) *
                      face_value / ratio)

        return int(votes)

    def vote_percent(self, date=None):
        """
        returns percentage of the users voting rights compared to total voting
        rights existing
        """
        if (self.is_company_shareholder() or
                not self.company.get_total_votes_floating()):
            return float(0.0)

        # do the math
        total_votes_eligible = self.company.get_total_votes_eligible()

        # how much percent of these eligible votes does the shareholder have?
        return (self.vote_count(date) /
                float(total_votes_eligible))


class Operator(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    company = models.ForeignKey('Company', verbose_name="Operators Company")
    share_count = models.PositiveIntegerField(blank=True, null=True)

    def __unicode__(self):
        return u"{} {} ({})".format(
            self.user.first_name, self.user.last_name, self.user.email)


class Security(models.Model):
    SECURITY_TITLES = (
        ('P', _('Preferred Stock')),
        ('C', _('Common Stock')),
        ('R', _('Registered Shares')),
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
        options = self.company.get_total_options(security=self)

        return total_shares - floating_shares - options

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


class Position(models.Model):
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
            return _('Share issue')
        return _('Regular Ownership change')


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


class OptionTransaction(models.Model):
    """ Transfer of options from someone to anyone """
    bought_at = models.DateField()
    buyer = models.ForeignKey('Shareholder', related_name="option_buyer")
    option_plan = models.ForeignKey('OptionPlan')
    count = models.PositiveIntegerField()
    seller = models.ForeignKey('Shareholder', blank=True, null=True,
                               related_name="option_seller")
    vesting_months = models.PositiveIntegerField(blank=True, null=True)
    certificate_id = models.CharField(
        max_length=255, blank=True, null=True,
        help_text=_('id of the issued certificate'))
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


# --------- DJANGO TAGGING ----------
register(Shareholder)


# --------- SIGNALS ----------
# must be inside a file which is imported by django on startup
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        UserProfile.objects.create(user=instance)
