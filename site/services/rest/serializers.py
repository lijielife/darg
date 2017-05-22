import logging
from dateutil.parser import parse as timeparse

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import mail_managers, send_mail
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import Q
from django.db.models.signals import post_save
from django.utils.translation import ugettext as _
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from services.rest.mixins import (FieldValidationMixin,
                                  SubscriptionSerializerMixin)
from reports.models import Report
from shareholder.models import (Bank, Company, Country, Operator, OptionPlan,
                                OptionTransaction, Position, Security,
                                Shareholder, UserProfile)
from utils.formatters import inflate_segments, string_list_to_json
from utils.hashers import random_hash
from utils.math import substract_list
from utils.session import get_company_from_request
from utils.user import make_username

User = get_user_model()
logger = logging.getLogger(__name__)


class CountrySerializer(serializers.HyperlinkedModelSerializer):
    """ list of countries selectable """

    class Meta:
        model = Country
        fields = ('url', 'iso_code', 'name')


class BankSerializer(serializers.HyperlinkedModelSerializer):
    """ list of countries selectable """
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Bank
        fields = ('pk', 'name', 'short_name', 'swift', 'address', 'city',
                  'postal_code', 'full_name')
        extra_kwargs = {'pk': {'read_only': False}}

    def get_full_name(self, obj):
        name = u"{} ({}, {}".format(
            obj.name, obj.city, obj.address)
        if obj.swift:
            name += u" | {})".format(obj.swift)
        else:
            name += u")"
        return name


class SecuritySerializer(serializers.HyperlinkedModelSerializer,
                         FieldValidationMixin):
    readable_title = serializers.SerializerMethodField()
    readable_number_segments = serializers.SerializerMethodField()

    class Meta:
        model = Security
        fields = ('pk', 'readable_title', 'title', 'url', 'count',
                  'track_numbers', 'readable_number_segments',
                  'number_segments', 'face_value', 'cusip')

    def get_readable_title(self, obj):
        if obj.face_value:
            return obj.get_title_display() + u' ({} CHF)'.format(
                int(obj.face_value))
        else:
            return obj.get_title_display()

    def get_readable_number_segments(self, obj):
        """
        change json into human readble format
        """
        return str(obj.number_segments).translate(None, "'[]u{}")

    def update(self, instance, validated_data):
        """
        handle saving human readable numbers segments format
        """
        number_segments = validated_data.get(
            'number_segments', instance.number_segments)
        instance.number_segments = number_segments
        instance.save()
        return instance


class CompanySerializer(SubscriptionSerializerMixin,
                        serializers.HyperlinkedModelSerializer):
    security_set = SecuritySerializer(many=True, read_only=True)
    country = serializers.HyperlinkedRelatedField(
        view_name='country-detail',
        required=False,
        allow_null=True,
        queryset=Country.objects.all(),
    )
    founded_at = serializers.DateField()
    profile_url = serializers.SerializerMethodField()
    logo_url = serializers.SerializerMethodField()
    vote_count = serializers.SerializerMethodField()
    vote_count_floating = serializers.SerializerMethodField()
    current_subscription = serializers.CharField(
        source='get_current_subscription_plan',
        read_only=True
    )
    has_address = serializers.BooleanField(read_only=True)

    class Meta:
        model = Company
        fields = ('pk', 'name', 'share_count',
                  'url',
                  # not needed as of now, adding one more db query
                  # 'shareholder_count',
                  'security_set', 'founded_at',
                  'provisioned_capital', 'profile_url',
                  'logo_url', 'email', 'has_address',
                  'is_statement_sending_enabled', 'statement_sending_date',
                  'vote_count', 'vote_ratio', 'vote_count_floating',
                  'current_subscription', 'subscription_features',
                  'subscription_permissions',
                  'send_shareholder_statement_via_letter_enabled',
                  'signatures',
                  ) + Company.ADDRESS_FIELDS

    def get_profile_url(self, obj):
        return reverse('company', kwargs={'company_id': obj.id})

    def get_logo_url(self, obj):
        return obj.get_logo_url()

    def get_vote_count(self, obj):
        return obj.get_total_votes()

    def get_vote_count_floating(self, obj):
        return obj.get_total_votes_floating()


class AddCompanySerializer(serializers.Serializer):

    name = serializers.CharField(max_length=255)
    face_value = serializers.DecimalField(max_digits=19, decimal_places=4,
                                          required=False)
    founded_at = serializers.DateTimeField(required=False)
    share_count = serializers.IntegerField()
    pk = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        """ check data, add company, add company_itself shareholder, add first
        position' """

        user = validated_data.get("user")

        # handle creation operation as an atomic transaction to not create an
        # inconsistent database
        with transaction.atomic():
            # for stripe payments company is the `subscriber`. it has to have an
            # email address which is used for sending the invoice to. we are
            # putting the email of the user which creates the company there
            company = Company.objects.create(
                share_count=validated_data.get("share_count"),
                name=validated_data.get("name"),
                founded_at=validated_data.get('founded_at'),
                email=self.context.get('request').user.email,
            )
            security = Security.objects.create(
                title="C",
                count=validated_data.get("share_count"),
                company=company,
                face_value=validated_data.get("face_value"),
            )

            username = make_username('Company', 'itself', company.name)
            # user tried to add company already
            if User.objects.filter(username=username).exists():
                username = username[:25] + u'-' + random_hash(digits=4)

            # create company user
            companyuser = User.objects.create(
                username=username,
                first_name=settings.COMPANY_INITIAL_FIRST_NAME,
                last_name=company.name[:30],
                email=u''  # [#208] - artificial email confused user
            )
            shareholder = Shareholder.objects.create(
                user=companyuser, company=company, number='0')
            Position.objects.create(
                bought_at=validated_data.get(
                    'founded_at') or timezone.now(),
                buyer=shareholder, count=validated_data.get("share_count"),
                value=validated_data.get("face_value"),
                security=security,
            )
            Operator.objects.create(user=user, company=company,
                                    last_active_at=timezone.now())

            mail_managers(
                u'new user signed up',
                u'user {} signed up for company {}'.format(user, company)
            )

            return company

    def validate_share_count(self, value):
        if value < 0:
            raise ValidationError(
                'share count "%s" must be larger then 0'.format(value))
        return value


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    """ serialize additional user data """
    # country = CountrySerializer(many=False)
    readable_language = serializers.SerializerMethodField()
    readable_legal_type = serializers.SerializerMethodField()
    birthday = serializers.DateTimeField(
        required=False, allow_null=True)

    class Meta:
        model = UserProfile
        fields = ('street', 'city', 'province', 'postal_code', 'country',
                  'birthday', 'company_name', 'language', 'readable_language',
                  'readable_legal_type', 'legal_type', 'company_department',
                  'title', 'salutation', 'street2', 'pobox', 'c_o',
                  'nationality', 'initial_registration_at')

    def get_readable_language(self, obj):
        return obj.get_language_display()

    def get_readable_legal_type(self, obj):
        return obj.get_legal_type_display()


class UserWithEmailOnlySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        # names used within company detail page
        fields = ('email', 'first_name', 'last_name')


class OperatorSerializer(serializers.HyperlinkedModelSerializer):
    # company = CompanySerializer(many=False, read_only=True)
    company = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=False,
        view_name='company-detail',
        queryset=Company.objects.all(),
    )
    is_myself = serializers.SerializerMethodField()
    user = UserWithEmailOnlySerializer()

    class Meta:
        model = Operator
        fields = (
            'id',
            'company',
            'is_myself',
            'user',
        )

    def get_is_myself(self, obj):
        return obj.user == self.context.get("request").user

    def create(self, validated_data):
        """ create new operator """
        if User.objects.filter(
            email=validated_data.get('user').get('email')
        ).exists():
            user = User.objects.get(
                email=validated_data.get('user').get('email'))
        else:
            raise ValidationError({'email': _(
                'User not yet registered with this '
                'application. Please ask the user to register first.'
            )})
        company = validated_data.get('company')
        myself = self.context.get("request").user
        if not myself.operator_set.filter(company=company):
            raise ValidationError({'company': _(
                'You cannot edit this company'
            )})

        # notify
        send_mail(
            _('You were added as administrator for {}').format(company.name),
            _('Dear,\n\n'
              'you have been granted edit privileges for this '
              'company on the share register\n\nKind regards\n\n'
              'Your Das-Aktienregister Team'),
            settings.SERVER_EMAIL,
            [user.email], fail_silently=False)

        return Operator.objects.create(user=user, company=company)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    userprofile = UserProfileSerializer(
        many=False, required=False, allow_null=True)
    selected_company = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'userprofile', 'selected_company')
        extra_kwargs = {'email': {'required': False, 'allow_blank': True}}

    def create(self, validated_data):

        if validated_data.get('user').get('userprofile'):
            userprofile_data = validated_data.pop('userprofile')
            userprofile = UserProfile.objects.create(**userprofile_data)
        else:
            raise ValidationError('Missing User Profile data')

        if validated_data.get('user').get('userprofile').get('country'):
            country_data = validated_data.get(
                'user').get('userprofile').get('country')
            country = Country.objects.create(**country_data)
        else:
            raise ValidationError('Missing country data')

        validated_data['user']['userprofile'] = userprofile
        validated_data['user']['userprofile']['country'] = country

        user = User.objects.create(**validated_data)

        return user

    def validate_email(self, value):
        """
        handle django user model not allowing None values
        """
        if not value:
            return u''
        else:
            return value

    def get_selected_company(self, obj):
        """
        return company the user selected last
        """

        try:
            op = Operator.objects.filter(
                user=obj,
                company__pk=get_company_from_request(self.context['request']).pk
            ).first()
        except ValueError:
            return None

        if op:
            return reverse('company-detail',
                           kwargs={'pk': op.company.pk})
        return None


class ShareholderListSerializer(serializers.HyperlinkedModelSerializer):
    """ made for performance, avoids any queries or nested data """
    # user = UserSerializer(many=False)
    full_name = serializers.SerializerMethodField()
    is_company = serializers.SerializerMethodField()

    class Meta:
        model = Shareholder
        fields = (
            'pk', 'number',
            # 'user',
            'share_percent',  # +2 queries/obj
            'share_count',  # +2 queries/obj
            'cumulated_face_value',
            'validate_gafi',
            'is_company',
            'full_name',
            # 'order_cache',  not needed as of now, for ordering only
        )

    def get_full_name(self, obj):
        return obj.get_full_name()

    def get_is_company(self, obj):
        return obj.is_company_shareholder()  # adds one query per obj


class ShareholderSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(many=False)
    company = CompanySerializer(many=False,  read_only=True)
    is_company = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    readable_mailing_type = serializers.SerializerMethodField()

    class Meta:
        model = Shareholder
        fields = (
            'pk', 'number',
            'user', 'company',
            'share_percent',  # +2 queries/obj
            'share_count',  # +2 queries/obj
            'share_value',
            'validate_gafi',
            'is_company',
            'full_name',
            'mailing_type',
            'readable_mailing_type',
            'vote_count', 'vote_percent',
            'is_management',
            'cumulated_face_value',
        )

    def create(self, validated_data):

        # FIXME: assuming one company per user
        company = get_company_from_request(self.context.get("request"))

        if not validated_data.get('user').get('first_name'):
            raise ValidationError({'first_name': [_('First Name missing')]})

        if not validated_data.get('user').get('last_name'):
            raise ValidationError({'last_name': [_('Last Name missing')]})

        if company.shareholder_set.filter(
            number=validated_data.get('number')
        ).exists():
            raise ValidationError(
                {'number': [_('Shareholder Number must be unique')]})

        # get unique username
        username = make_username(
            validated_data.get("user", {}).get("first_name", u''),
            validated_data.get("user", {}).get("last_name", u''),
            validated_data.get("user", {}).get("email", u'')
        )
        email = validated_data.get("user", {}).get("email", u'')
        if email:
            user_kwargs = {'email': email}
        else:
            user_kwargs = {'username': username}

        shareholder_user, created = User.objects.get_or_create(
            defaults={
                "email": validated_data.get("user", {}).get("email", u''),
                "first_name": validated_data.get("user").get("first_name"),
                "last_name": validated_data.get("user").get("last_name"),
                "username": username,
            },
            **user_kwargs
        )

        if not hasattr(shareholder_user, 'userprofile'):
            shareholder_user.userprofile = UserProfile.objects.create()

        if not created:
            if not shareholder_user.first_name:
                shareholder_user.first_name = validated_data.get(
                    "user").get("first_name")
            if not shareholder_user.last_name:
                shareholder_user.last_name = validated_data.get(
                    "user").get("last_name")
            shareholder_user.save()

        # save shareholder
        shareholder, created = Shareholder.objects.get_or_create(
            user=shareholder_user,
            company=company,
            defaults={"number": validated_data.get("number")},
        )

        # fire signal to update order_cache
        post_save.send(
            Shareholder, instance=shareholder, using='default', created=True)

        return shareholder

    def is_valid(self, raise_exception=False):

        res = super(ShareholderSerializer, self).is_valid(raise_exception)

        initial_data = self.initial_data
        self._validate_email(initial_data.get('user', {}).get('email'))

        return res

    def update(self, instance, validated_data):

        shareholder = instance
        user = shareholder.user

        # don't create duplicate users with same email if email is set:
        if (
                validated_data['user'].get('email', u'') and
                User.objects.filter(
                    email=validated_data['user']['email']
                ).exists() and User.objects.get(
                    email=validated_data['user']['email']
                ) != user):
            raise ValidationError({'email': [_(
                'This email is already taken by another user/shareholder.')]})

        user.email = validated_data['user'].get('email', u'')
        user.first_name = validated_data['user']['first_name']
        user.last_name = validated_data['user']['last_name']
        user.save()

        profile_kwargs = validated_data['user']['userprofile']
        if not hasattr(user, 'userprofile'):
            userprofile = UserProfile.objects.create(**profile_kwargs)
            user.userprofile = userprofile
            user.save()
        else:
            userprofile = user.userprofile
            userprofile.street = profile_kwargs.get('street')
            userprofile.street2 = profile_kwargs.get('street2')
            userprofile.city = profile_kwargs.get('city')
            userprofile.province = profile_kwargs.get('province')
            userprofile.postal_code = profile_kwargs.get('postal_code')
            userprofile.pobox = profile_kwargs.get('pobox')
            userprofile.c_o = profile_kwargs.get('c_o')
            userprofile.country = profile_kwargs.get('country')
            userprofile.nationality = profile_kwargs.get('nationality')
            userprofile.company_name = profile_kwargs.get('company_name')
            userprofile.company_department = profile_kwargs.get(
                'company_department')
            userprofile.birthday = profile_kwargs.get('birthday')
            userprofile.language = profile_kwargs.get('language')
            userprofile.legal_type = profile_kwargs.get('legal_type') or 'H'
            userprofile.title = profile_kwargs.get('title')
            userprofile.salutation = profile_kwargs.get('salutation')
            userprofile.save()

        shareholder.number = validated_data['number']
        shareholder.is_management = validated_data['is_management']
        if 'mailing_type' in validated_data.keys():
            shareholder.mailing_type = validated_data['mailing_type']
        shareholder.save()
        return shareholder

    def get_is_company(self, obj):
        return obj.is_company_shareholder()  # adds one query per obj

    def get_full_name(self, obj):
        return obj.get_full_name()

    def get_readable_mailing_type(self, obj):
        """
        change make it readable
        """
        return obj.get_mailing_type_display()

    def _validate_email(self, value):
        """ email cann only be used once or never """
        # can stay empty
        if not value:
            return value

        error = ValidationError(
            {'email': [_('shareholder with this email already exists')]})

        # different on update/create
        company = get_company_from_request(self.context.get('request'))
        if self.instance:
            if company.shareholder_set.filter(
                    user__email=value).exclude(pk=self.instance.pk).exists():
                raise error
            return

        if company.shareholder_set.filter(user__email=value).exists():
            raise error

    def validate_number(self, value):
        """
        we must not have duplicate numbers per company, ensure that for update
        operations the current sh obj is excluded
        """
        if not value:
            return value

        if self.context.get("request"):
            request = self.context.get("request")
            qs = Shareholder.objects.filter(
                company=get_company_from_request(request),
                number=value)
            # for update operations
            if self.instance is not None and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            # fail if number is used
            if qs.exists():
                raise serializers.ValidationError(
                    _('Number must be unique for this company'))

        return value


class PositionSerializer(serializers.HyperlinkedModelSerializer,
                         FieldValidationMixin):

    buyer = ShareholderListSerializer(many=False, required=False)
    seller = ShareholderListSerializer(many=False, required=False)
    security = SecuritySerializer(many=False, required=True)
    depot_bank = BankSerializer(many=False, required=False)
    bought_at = serializers.DateTimeField()  # e.g. 2015-06-02T23:00:00.000Z
    readable_number_segments = serializers.SerializerMethodField()
    readable_registration_type = serializers.SerializerMethodField()
    readable_depot_type = serializers.SerializerMethodField()
    position_type = serializers.SerializerMethodField()
    certificate_invalidation_position_url = serializers.SerializerMethodField()
    certificate_invalidation_initial_position_url = \
        serializers.SerializerMethodField()
    is_certificate_valid = serializers.SerializerMethodField()

    class Meta:
        model = Position
        fields = (
            'pk', 'buyer', 'seller', 'bought_at', 'count', 'value',
            'security', 'comment', 'is_split', 'is_draft', 'number_segments',
            'readable_number_segments', 'registration_type',
            'readable_registration_type', 'position_type', 'depot_type',
            'readable_depot_type', 'stock_book_id', 'vesting_months',
            'certificate_id', 'printed_at', 'depot_bank',
            'certificate_invalidation_position_url',
            'certificate_invalidation_initial_position_url',
            'is_certificate_valid')

    def _get_company(self):
        company = get_company_from_request(self.context.get("request"))
        return company

    def get_certificate_invalidation_position_url(self, obj):
        if obj.certificate_invalidation_position:
            return reverse(
                'position',
                kwargs={'pk': obj.certificate_invalidation_position.pk})

    def get_certificate_invalidation_initial_position_url(self, obj):
        if hasattr(obj, 'certificate_initial_position'):
            return reverse(
                'position',
                kwargs={'pk': obj.certificate_initial_position.pk})

    def get_is_certificate_valid(self, obj):
        if not obj.certificate_id:
            return
        if obj.certificate_invalidation_position:
            return False
        if hasattr(obj, 'certificate_initial_position'):
            return False
        else:
            return True

    def get_readable_number_segments(self, obj):
        """
        change json into human readble format
        """
        return str(obj.number_segments).translate(None, "'[]u{}")

    def get_readable_registration_type(self, obj):
        """
        change make it readable
        """
        return obj.get_registration_type_display()

    def get_readable_depot_type(self, obj):
        """
        change make it readable
        """
        return obj.get_depot_type_display()

    def get_position_type(self, obj):
        return obj.get_position_type()

    def is_valid(self, raise_exception=False):
        """
        validate cross data relations
        """

        logger.info('position create validation...')

        res = super(PositionSerializer, self).is_valid(raise_exception)

        initial_data = self.initial_data
        security = initial_data.get('security')
        company = get_company_from_request(self.context.get("request"))

        # --- TRACK NUMBERS validation
        if security and Security.objects.get(
                company=company, pk=security.get('pk')).track_numbers:

            self._validate_number_segments(company, security, initial_data)

        return res

    def create(self, validated_data):
        """ adding a new position and handling nested data for buyer
        and seller """

        logger.info('position create ...')

        # prepare data
        kwargs = {}
        company = get_company_from_request(self.context.get("request"))

        security = Security.objects.get(
            company=company,
            title=validated_data.get('security').get('title'),
            face_value=validated_data.get('security').get('face_value')
        )

        # ------- regular security transaction
        if validated_data.get("seller") and validated_data.get("buyer"):
            buyer = Shareholder.objects.get(
                company=company,
                number=validated_data.get(
                    "buyer").get("number")
            )
            seller = Shareholder.objects.get(
                company=company,
                number=validated_data.get(
                    "seller").get("number")
            )
            kwargs.update({"seller": seller, 'registration_type': '2'})

        # -------- capital increase
        else:
            buyer = company.get_company_shareholder()
            company.share_count = company.share_count + \
                validated_data.get("count")

            # add new number segments to company register
            if security.track_numbers:
                segs = validated_data.get('number_segments')
                security.number_segments.extend(segs)
                security.save()

            company.save()
            kwargs.update({'registration_type': '1'})

        # ------- common logic
        kwargs.update({
            "buyer": buyer,
            "bought_at": validated_data.get("bought_at"),
            "value": validated_data.get("value"),
            "count": validated_data.get("count"),
            "security": security,
            "comment": validated_data.get("comment"),
        })

        # segments must be ordered, have no duplicates and must be list...
        if security.track_numbers and validated_data.get("number_segments"):
            kwargs.update({
                "number_segments": validated_data.get("number_segments")
            })

        if validated_data.get("stock_book_id"):
            kwargs.update({
                'stock_book_id': validated_data.get("stock_book_id")})

        if validated_data.get("depot_type"):
            kwargs.update({
                'depot_type': validated_data.get("depot_type")})

        if validated_data.get("vesting_months"):
            kwargs.update({
                'vesting_months': validated_data.get("vesting_months")})

        if validated_data.get("certificate_id"):
            kwargs.update({
                'certificate_id': validated_data.get("certificate_id")})

        if validated_data.get("depot_bank"):
            kwargs.update({
                'depot_bank': Bank.objects.get(
                    pk=validated_data.get("depot_bank")['pk'])})

        position = Position.objects.create(**kwargs)

        # fire signal to update order_cache
        post_save.send(
            Position, instance=position, using='default', created=True)

        return position

    def validate_certificate_id(self, value):
        """
        ensure that its unique
        """
        if not value:
            return value

        company = self._get_company()
        ot_queryset = OptionTransaction.objects.filter(
            option_plan__company=company, certificate_id=value)
        pos_queryset = Position.objects.filter(
            Q(buyer__company=company) | Q(seller__company=company),
            certificate_id=value)
        # exclude self on update operation
        if self.instance is not None and self.instance.pk:
            pos_queryset = pos_queryset.exclude(pk=self.instance.pk).exists()

        # if not yet existing
        if not ot_queryset.exists() and not pos_queryset.exists():
            return value
        else:
            raise ValidationError(
                _("Certificate ID {} is already used in transaction or option "
                  "transaction").format(value))

    def validate_count(self, value):
        """
        shareholder cannot sell what he doesn't own
        """
        value = float(value)
        if value < 0:
            raise ValidationError(_('count {} must be greater then 0'
                                    '').format(value))

        # seller is optional
        if self.initial_data.get('seller'):
            security = Security.objects.get(
                pk=self.initial_data.get('security').get('pk'))
            seller = Shareholder.objects.get(
                pk=self.initial_data.get('seller').get('pk'))

            # does the seller have enough shares to sell?
            bought_at = (self.initial_data.get('bought_at') or
                         timezone.now().date().isoformat())
            sellable_shares = seller.share_count_sellable(
                security=security,
                date=timeparse(bought_at))
            if value > sellable_shares:
                raise ValidationError(
                    _('seller does not have enough shares. max value is {}. '
                      'shares can be blocked by cert depot or vesting.').format(
                        sellable_shares))

        return value

    def validate_depot_bank(self, value):
        """
        bank is needed if certificate depot is selected
        """
        if self.initial_data.get('depot_type') == '0':
            if not value:
                raise ValidationError(
                    _('Depot bank is mandatory if depot type is certificate '
                      'depot'
                      ''))
        return value

    def _validate_number_segments(self, company, security,
                                  raise_exception=False):
        initial_data = self.initial_data
        security = Security.objects.get(company=company, pk=security.get('pk'))
        logger.info('validation: prepare data...')
        if (isinstance(initial_data.get('number_segments'), str) or
                isinstance(initial_data.get('number_segments'), unicode)):
            segments = string_list_to_json(
                initial_data.get('number_segments'))
        else:
            segments = initial_data.get('number_segments')

        # if we have seller (non capital increase)
        if initial_data.get('seller'):
            logger.info('validation: get seller segments...')
            seller = Shareholder.objects.get(
                pk=initial_data.get('seller')['pk'])
            owning, failed_segments, owned_segments = seller.owns_segments(
                segments, security)
            logger.info(
                'validation: seller segs {} for security {} done'.format(
                    segments, security))

        # we need number_segments if this is a security with .track_numbers
        if not segments:
            raise serializers.ValidationError(
                {'number_segments':
                    [_('Invalid security numbers segments.')]})

        # segments must be owned by seller
        elif initial_data.get('seller') and not owning:
            raise serializers.ValidationError({
                'number_segments':
                    [_('Segments "{}" must be owned by seller "{}". '
                       'Available are {}').format(
                          failed_segments, seller.user.last_name,
                          owned_segments
                    )]
            })

        # validate segment count == share count
        elif (security.count_in_segments(segments) !=
                initial_data.get('count')):
            logger.info('validation: checking count...')
            raise serializers.ValidationError({
                'count':
                    [_('Number of shares in segments ({}) '
                       'does not match count {}').format(
                            security.count_in_segments(segments),
                            initial_data.get('count')
                       )]
            })

        # segment must not be used by option plan
        logger.info('validation: option plan validation...')
        inflated_segments = inflate_segments(segments)
        oplan_segments = inflate_segments(
            security.company.get_all_option_plan_segments())
        if substract_list(
            inflated_segments, oplan_segments
        ) != inflated_segments:
            raise serializers.ValidationError({
                'number_segments':
                    [_('Segment {} is blocked for options and cannot be'
                       ' transfered to a shareholder.').format(segments)]
            })


class OptionPlanSerializer(serializers.HyperlinkedModelSerializer):
    """
    excluded `optiontransaction_set` to speed up performance
    """
    security = SecuritySerializer(many=False, required=True)
    # optiontransaction_set = OptionTransactionSerializer(many=True,
    #                                                     read_only=True)
    board_approved_at = serializers.DateField()
    readable_number_segments = serializers.SerializerMethodField()

    class Meta:
        model = OptionPlan
        fields = ('pk', 'title', 'security',  # 'optiontransaction_set',
                  'exercise_price', 'count', 'comment', 'board_approved_at',
                  'url', 'pdf_file', 'pdf_file_preview_url', 'pdf_file_url',
                  'number_segments', 'readable_number_segments')

    def validate_pdf_file(self, value):
        if not value:
            return

        if value.content_type == 'application/pdf':
            return value
        else:
            raise serializers.ValidationError(_("Not a pdf file."))

    def create(self, validated_data):

        # prepare data
        kwargs = {}
        company = get_company_from_request(self.context.get("request"))
        security = Security.objects.get(
            company=company,
            title=validated_data.get("security").get('title'),
            face_value=validated_data.get("security").get('face_value'))

        kwargs.update({
            "company": company,
            "board_approved_at": validated_data.get("board_approved_at"),
            "title": validated_data.get("title"),
            "security": security,
            "count": validated_data.get("count"),
            "exercise_price": validated_data.get("exercise_price"),
            "comment": validated_data.get("comment"),
        })

        # segments must be ordered, have no duplicates and must be list...
        if security.track_numbers and validated_data.get("number_segments"):
            kwargs.update({
                "number_segments": string_list_to_json(
                    validated_data.get("number_segments"))
            })

        option_plan = OptionPlan.objects.create(**kwargs)

        # assign all initial options to company shareholder
        cs = company.get_company_shareholder()
        kwargs = {
            'option_plan': option_plan,
            'bought_at': validated_data.get("board_approved_at"),
            'buyer': cs,
            'count': validated_data.get("count")
        }

        # segments must be ordered, have no duplicates and must be list...
        if security.track_numbers and validated_data.get("number_segments"):
            kwargs.update({
                "number_segments": string_list_to_json(
                    validated_data.get("number_segments"))
            })

        OptionTransaction.objects.create(**kwargs)

        return option_plan

    def get_readable_number_segments(self, obj):
        """
        change json into human readble format
        """
        return str(obj.number_segments).translate(None, "'[]u{}")

    def is_valid(self, raise_exception=False):
        """
        validate cross data relations
        """
        res = super(OptionPlanSerializer, self).is_valid(raise_exception)

        initial_data = self.initial_data

        security = initial_data.get('security')
        if security and Security.objects.get(id=security['pk']).track_numbers:

            security = Security.objects.get(id=security['pk'])
            if (isinstance(initial_data.get('number_segments'), str) or
                    isinstance(initial_data.get('number_segments'), unicode)):
                segments = string_list_to_json(
                    initial_data.get('number_segments'))
            else:
                segments = initial_data.get('number_segments')

            # we need number_segments if this is a security with .track_numbers
            if not segments:
                raise serializers.ValidationError(
                    {'number_segments':
                        [_('Invalid or empty security numbers segments.')]})

            # segments must be available by company shareholder
            cs = security.company.get_company_shareholder()
            owning, failed_segments, owned_segments = cs.owns_segments(
                    segments, security)

            # segments must be owned by seller
            if not owning:
                raise serializers.ValidationError({
                    'number_segments':
                        [_('Segments "{}" must be owned by company shareholder '
                           '"{}". Available are {}').format(
                              failed_segments, cs.user.last_name,
                              owned_segments
                        )]
                })

            # validate segment count == share count
            elif (security.count_in_segments(segments) !=
                    initial_data.get('count')):
                raise serializers.ValidationError({
                    'count':
                        [_('Number of shares in segments ({}) '
                           'does not match count {}').format(
                                security.count_in_segments(segments),
                                initial_data.get('count')
                           )]
                })

        return res


class OptionTransactionSerializer(serializers.HyperlinkedModelSerializer):
    buyer = ShareholderListSerializer(many=False, required=True)
    seller = ShareholderListSerializer(many=False, required=True)
    bought_at = serializers.DateField()  # e.g. 2015-06-02T23:00:00.000Z
    readable_number_segments = serializers.SerializerMethodField()
    readable_registration_type = serializers.SerializerMethodField()
    readable_depot_type = serializers.SerializerMethodField()
    option_plan = OptionPlanSerializer()

    class Meta:
        model = OptionTransaction
        fields = ('pk', 'buyer', 'seller', 'bought_at', 'count', 'option_plan',
                  'is_draft', 'number_segments', 'readable_number_segments',
                  'readable_registration_type', 'registration_type',
                  'depot_type', 'readable_depot_type', 'stock_book_id',
                  'certificate_id', 'printed_at')

    def _get_optionplan(self):
        op_serialized = self.initial_data.get('option_plan')
        if isinstance(op_serialized, dict):
            pk = op_serialized.get('pk')
        else:
            pk = int(op_serialized.split('/')[-1])
        option_plan = OptionPlan.objects.get(id=pk)
        return option_plan

    def is_valid(self, raise_exception=False):
        """
        validate cross data relations
        """
        res = super(OptionTransactionSerializer, self).is_valid(raise_exception)

        initial_data = self.initial_data

        option_plan = self._get_optionplan()
        security = option_plan.security

        if not security.track_numbers:
            return res

        if (isinstance(initial_data.get('number_segments'), str) or
                isinstance(initial_data.get('number_segments'), unicode)):
            segments = string_list_to_json(initial_data.get('number_segments'))
        else:
            segments = initial_data.get('number_segments')

        # we need number_segments if this is a security with .track_numbers
        if not segments:
            raise serializers.ValidationError(
                {'number_segments':
                    [_('Invalid security numbers segments.')]})

        # if we have seller (non capital increase)
        if initial_data.get('seller'):
            seller = Shareholder.objects.get(
                pk=initial_data.get('seller')['pk'])
            owning, failed_segments, owned_segments = seller.\
                owns_options_segments(segments, security)

        # segments must be owned by seller
        if initial_data.get('seller') and not owning:
            raise serializers.ValidationError({
                'number_segments':
                    [_('Segments "{}" must be owned by seller "{}". '
                       'Available are {}').format(
                          failed_segments, seller.user.last_name,
                          owned_segments
                    )]
            })

        # validate segment count == share count
        elif (security.count_in_segments(segments) !=
                initial_data.get('count')):
            raise serializers.ValidationError({
                'count':
                    [_('Number of shares in segments ({}) '
                       'does not match count {}').format(
                            security.count_in_segments(segments),
                            initial_data.get('count')
                       )]
            })

        # segments must be inside option plans segments
        for segment in inflate_segments(segments):
            if segment not in inflate_segments(option_plan.number_segments):
                raise serializers.ValidationError({
                    'number_segments':
                        [_('Segment {} is not reserved for options inside a'
                           ' option plan and cannot be'
                           ' transfered to a option holder. Available are: '
                           '{}').format(segment, option_plan.number_segments)]
                })

        return res

    def create(self, validated_data):

        # prepare data
        kwargs = {}
        company = get_company_from_request(self.context.get("request"))
        option_plan = OptionPlan.objects.get(
            pk=self.initial_data.get('option_plan').get('pk'))

        buyer = Shareholder.objects.get(
            company=company,
            number=validated_data.get(
                "buyer").get("number")
        )
        seller = Shareholder.objects.get(
            company=company,
            number=validated_data.get(
                "seller").get("number")
        )
        kwargs.update({"seller": seller})
        kwargs.update({"buyer": buyer})

        kwargs.update({
            "bought_at": validated_data.get("bought_at"),
            "count": validated_data.get("count"),
            "option_plan": option_plan,
            "vesting_months": validated_data.get("vesting_months"),
            "registration_type": '2',
        })

        # segments must be ordered, have no duplicates and must be list...
        if (option_plan.security.track_numbers and
                validated_data.get("number_segments")):

            kwargs.update({
                "number_segments": string_list_to_json(
                    validated_data.get("number_segments"))
            })

        if validated_data.get("stock_book_id"):
            kwargs.update({
                'stock_book_id': validated_data.get("stock_book_id")})

        if validated_data.get("depot_type"):
            kwargs.update({
                'depot_type': validated_data.get("depot_type")})

        if validated_data.get("certificate_id"):
            kwargs.update({
                'certificate_id': validated_data.get("certificate_id")})

        option_transaction = OptionTransaction.objects.create(**kwargs)

        # fire signal to update order_cache
        post_save.send(
            OptionTransaction, instance=option_transaction, using='default',
            created=True)

        return option_transaction

    def get_readable_number_segments(self, obj):
        """
        change json into human readble format
        """
        return str(obj.number_segments).translate(None, "'[]u{}")

    def get_readable_registration_type(self, obj):
        """
        change make it readable
        """
        return obj.get_registration_type_display()

    def get_readable_depot_type(self, obj):
        """
        change make it readable
        """
        return obj.get_depot_type_display()

    def validate_certificate_id(self, value):
        """
        ensure that its unique
        """
        if not value:
            return value

        company = self._get_optionplan().company
        ot_queryset = OptionTransaction.objects.filter(
            option_plan__company=company, certificate_id=value)
        pos_queryset = Position.objects.filter(
            Q(buyer__company=company) | Q(seller__company=company),
            certificate_id=value)
        # exclude self on update operation
        if self.instance is not None and self.instance.pk:
            ot_queryset = ot_queryset.exclude(pk=self.instance.pk).exists()

        # if not yet existing
        if not ot_queryset.exists() and not pos_queryset.exists():
            return value
        else:
            raise ValidationError(
                _("Certificate ID {} is already used in transaction or option "
                  "transaction").format(value))

    def validate_count(self, value):
        """
        shareholder cannot sell what he doesn't own
        """
        value = float(value)
        if value < 0:
            raise ValidationError(_('count {} must be greater then 0'
                                    '').format(value))

        # seller is optional
        if self.initial_data.get('seller'):
            security = Security.objects.get(
                pk=self.initial_data.get('option_plan')['security']['pk'])
            seller = Shareholder.objects.get(
                pk=self.initial_data.get('seller').get('pk'))

            if value > seller.options_count(security=security):
                raise ValidationError(
                    _('seller does not have enough options. max value is {}.'
                      '').format(seller.options_count(security=security)))

        return value


class OptionHolderSerializer(serializers.HyperlinkedModelSerializer):
    """ commented some fields for the sake of performance """
    # user = UserSerializer(many=False)
    # company = CompanySerializer(many=False,  read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Shareholder
        fields = (
            'pk',
            # 'user',
            'number',
            # 'company',
            'options_percent',
            'options_count',
            # 'options_value',
            'full_name'
        )

    def get_full_name(self, obj):
        return obj.get_full_name()


class ReportSerializer(serializers.HyperlinkedModelSerializer):
    """ representing a generated report """
    url = serializers.SerializerMethodField()

    class Meta:
        fields = ('file_type', 'report_type', 'order_by', 'url', 'created_at',
                  'eta', 'company', 'user', 'downloaded_at', 'generated_at',
                  'report_at')
        model = Report
        extra_kwargs = {
            'url': {'read_only': True},
            'created_at': {'read_only': True},
            'eta': {'read_only': True},
            'company': {'read_only': True},
            'user': {'read_only': True},
            'downloaded_at': {'read_only': True},
            'generated_at': {'read_only': True},
        }

    def get_url(self, obj):
        """ return file download url """
        if obj.file:
            return reverse('reports:download', kwargs={'report_id': obj.pk})
        return ''
