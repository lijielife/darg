import datetime
import logging
import math
import os
import time
from collections import Counter
from decimal import Decimal

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import select_template
from django.utils.formats import date_format
from django.utils.text import slugify
from django.utils.translation import ugettext as _, activate as activate_lang
from django_languages import fields as language_fields
from rest_framework.authtoken.models import Token
from sorl.thumbnail import get_thumbnail
from dateutil.relativedelta import relativedelta

from utils.formatters import (deflate_segments, flatten_list,
                              human_readable_segments, inflate_segments,
                              string_list_to_json)
from utils.math import substract_list
from utils.pdf import render_pdf

from .mixins import AddressModelMixin
from .validators import validate_remote_email_id


logger = logging.getLogger(__name__)


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


def get_company_logo_upload_path(instance, filename):
    return os.path.join(
        "public", "company", "%d" % instance.id, "logo", filename)


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
    email = models.EmailField(_('Email'), blank=True)  # required by djstripe

    is_statement_sending_enabled = models.BooleanField(
        _('Is statement sending enabled'), default=True)
    statement_sending_date = models.DateField(_('statement sending date'),
                                              null=True, blank=True)

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

    def get_active_shareholders(self, date=None):
        """ returns list of all active shareholders """
        shareholder_list = []
        for shareholder in self.shareholder_set.all().order_by('number'):
            if shareholder.share_count(date=date) > 0:
                shareholder_list.append(shareholder)

        return shareholder_list

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
        return oh_list

    def get_all_option_plan_segments(self):
        """
        return list of number segments reserved for all option plans for
        this company
        """
        segments = self.optionplan_set.all().values_list(
            'number_segments', flat=True)
        return flatten_list(segments)

    def get_company_shareholder(self):
        return self.shareholder_set.earliest('id')

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
            val += position.count * position.value

        cap_destroying_positions = Position.objects.filter(
            seller__company=self, buyer__isnull=True)

        for position in cap_destroying_positions:
            val -= position.count * position.value

        return val

    def get_logo_url(self):
        """ return url for logo """
        if not self.logo:
            return

        kwargs = {'crop': 'center', 'quality': 99, 'format': "PNG"}
        return get_thumbnail(self.logo.file, 'x40', **kwargs).url

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
        value = float(company_shareholder.last_traded_share_price(
            date=execute_at, security=security))
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
                'value': value / divisor * dividend,
                'security': security,
                'bought_at': execute_at,
                'is_split': True,
                'comment': _('Share split of {} on {} with ratio {}:{}. '
                             'Provisioning of new shares.').format(
                                 security, execute_at.date(),
                                 int(dividend), int(divisor)),
            }
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


class UserProfile(AddressModelMixin, models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL)

    language = language_fields.LanguageField(blank=True, null=True)

    company_name = models.CharField(max_length=255, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)

    ip = models.GenericIPAddressField(blank=True, null=True)
    tnc_accepted = models.BooleanField(default=False)

    def __unicode__(self):
        return u"%s, %s %s" % (self.city, self.province, self.country)

    class Meta:
        verbose_name_plural = "UserProfile"


class Shareholder(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    company = models.ForeignKey('Company', verbose_name="Shareholders Company")
    number = models.CharField(max_length=255)

    def __unicode__(self):
        return u'{}'.format(self.id)

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
        return Shareholder.objects.filter(
            company=self.company).earliest('id').id == self.id

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
        date = date or datetime.datetime.now()
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

        return count_bought - count_sold

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

    def get_user_name(self):
        """
        returns full name of user if given, else email
        """
        return self.user.get_full_name() or self.user.email

    user_name = property(get_user_name)


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
        # ('O', 'Option'),
        # ('W', 'Warrant'),
        # ('V', 'Convertible Instrument'),
    )
    title = models.CharField(max_length=1, choices=SECURITY_TITLES)
    face_value = models.DecimalField(
        _('Nominal value of this asset'),
        max_digits=16, decimal_places=8, blank=True,
        null=True)
    company = models.ForeignKey(Company)
    count = models.PositiveIntegerField()
    number_segments = JSONField(
        _('JSON list of segments of ids for securities. can be 1, 2, 3, 4-10'),
        default=list)

    # settings
    track_numbers = models.BooleanField(
        _('App needs to track IDs of shares. WARNING: update initial '
          'transaction with segments on enabling.'), default=False)

    def __unicode__(self):
        return u"{} ({})".format(self.get_title_display(), self.company)

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
    is_split = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=True)
    number_segments = JSONField(
        _('JSON list of segments of ids for securities. can be 1, 2, 3, 4-10'),
        default=list, blank=True, null=True)
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
    number_segments = JSONField(
        _('JSON list of segments of ids for securities. can be 1, 2, 3, 4-10'),
        default=list, blank=True, null=True)
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


class ShareholderStatementReport(models.Model):
    """
    report for company regarding all shareholder statements
    """
    company = models.ForeignKey('Company', verbose_name=_('company'))
    report_date = models.DateField(_('report date'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('shareholder statement report')
        verbose_name_plural = _('shareholder statement reports')

    def __unicode__(self):
        return u'{} - {}'.format(self.company, date_format(self.report_date))

    def get_statement_count(self):
        """
        get count of all related ShareholderStatements
        """
        return self.shareholderstatement_set.count()

    statement_count = property(get_statement_count)

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

    def generate_statements(self):
        """
        generate statements for shareholder users of company,
        then set the statement_sending_date on company to next year
        TODO: check subscription
        """
        shareholders = self.company.shareholder_set.all()
        users = get_user_model().objects.filter(
            pk__in=shareholders.values_list('user_id', flat=True))
        for user in users:
            statement, created = self._create_shareholder_statement_for_user(
                user)
            if created:
                statement.send_email_notification()

        # set new sending date
        if self.company.statement_sending_date:
            self.company.statement_sending_date += relativedelta(
                year=self.company.statement_sending_date.year + 1)
            self.company.save()

    def _get_statement_pdf_path_for_user(self, user, report):
        """
        returns a unique directory path to for the user
        """
        path = os.path.join(settings.SHAREHOLDER_STATEMENT_ROOT,
                            str(user.pk),
                            str(report.company.pk),
                            str(report.report_date.year))
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

        pdf_dir = self._get_statement_pdf_path_for_user(user, self)
        pdf_filename = u'{}-{}-{}.pdf'.format(
            slugify(user.get_full_name() or user.email),
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
                user_name=user.get_full_name() or user.email,
                shareholder_list=self.company.shareholder_set.filter(
                    user_id=user.pk),
                site=Site.objects.get_current(),
                STATIC_URL=settings.STATIC_URL
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
        pdf = render_pdf(self.company.statement_template.render(context))

        if not pdf:
            return False

        with open(filepath, 'w') as f:
            f.write(pdf.getvalue())

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

    class Meta:
        verbose_name = _('shareholder statement')
        verbose_name_plural = _('shareholder statements')
        unique_together = ('report', 'user')

    def __unicode__(self):
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
        url = reverse('statement_download_pdf', args=[self.pk])
        if with_auth_token:
            url += u'?token={}'.format(self.user.auth_token.key)
        if absolute:
            url = u'{}://{}{}'.format(
                (getattr(settings, 'FORCE_SECURE_CONNECTION',
                         not settings.DEBUG) and 'https' or 'http'),
                Site.objects.get_current().domain, url)
        return url

    pdf_download_url = property(get_pdf_download_url)


# --------- SIGNALS ----------
# must be inside a file which is imported by django on startup
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        UserProfile.objects.create(user=instance)
