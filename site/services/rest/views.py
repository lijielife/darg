import dateutil.parser
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models import Q
from django.db.models.expressions import RawSQL
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.translation import ugettext as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, pagination, status, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from company.mixins import SubscriptionViewMixin
from reports.models import Report
from services.rest.pagination import SmallPagePagination
from services.rest.permissions import (HasSubscriptionPermission,
                                       IsOperatorPermission,
                                       UserCanAddCompanyPermission)
from services.rest.serializers import (AddCompanySerializer, BankSerializer,
                                       CompanySerializer, CountrySerializer,
                                       OperatorSerializer,
                                       OptionHolderSerializer,
                                       OptionPlanSerializer,
                                       OptionTransactionSerializer,
                                       PositionSerializer, ReportSerializer,
                                       SecuritySerializer,
                                       ShareholderListSerializer,
                                       ShareholderSerializer, UserSerializer,
                                       UserWithEmailOnlySerializer)
from shareholder.models import (Bank, Company, Country, Operator, OptionPlan,
                                OptionTransaction, Position, Security,
                                Shareholder)
from shareholder.tasks import update_order_cache_task
from utils.session import get_company_from_request

User = get_user_model()


# --- VIEWSETS

class CompanyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # FIXME filter by user perms
    queryset = Company.objects.all()
    pagination_class = SmallPagePagination
    serializer_class = CompanySerializer
    permission_classes = [
        IsOperatorPermission,
        HasSubscriptionPermission,
    ]
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('user__first_name', 'user__last_name', 'user__email',
                     'number')
    ordering_fields = ('user__last_name', 'user__email', 'number')

    def get_queryset(self):
        return Company.objects.filter(operator__user=self.request.user)

    @detail_route(methods=['post'])
    def upload(self, request, pk=None):
        obj = self.get_object()
        # FIXME: probably need some validation!
        obj.logo = request.FILES['logo']
        obj.save()
        return Response(CompanySerializer(
            obj,
            context={'request': request}).data,
            status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        """
        delete company
        """
        session = request.session
        del session['company_pk']
        session.save()
        return super(CompanyViewSet, self).destroy(request, pk)


class OperatorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # FIXME filter by user perms
    serializer_class = OperatorSerializer
    permission_classes = [
        IsOperatorPermission,
        HasSubscriptionPermission,
    ]
    queryset = Operator.objects.none()

    def get_queryset(self):
        company = get_company_from_request(self.request)
        return Operator.objects.filter(company=company)\
            .exclude(user__is_superuser=True).distinct()

    def destroy(self, request, pk=None):
        operator = self.get_object()
        user_operators = request.user.operator_set.all()
        # cannot remove himself
        if operator not in user_operators:
            # user can only edit corps he manages
            company_ids = user_operators.values_list(
                'company_id', flat=True).distinct()
            if operator.company_id in company_ids:
                operator.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        # else:
        return Response(status=status.HTTP_403_FORBIDDEN)


class PositionViewSet(SubscriptionViewMixin, viewsets.ModelViewSet):
    """ API endpoint to get positions """
    serializer_class = PositionSerializer
    pagination_class = SmallPagePagination
    permission_classes = [
        IsOperatorPermission,
        HasSubscriptionPermission
    ]
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('buyer__user__first_name', 'buyer__user__last_name',
                     'buyer__user__email',
                     'buyer__user__userprofile__company_name',
                     'seller__user__first_name',
                     'seller__user__last_name', 'seller__user__email',
                     'seller__number', 'buyer__number',
                     'seller__user__userprofile__company_name',
                     'bought_at', 'comment', 'seller__number', 'buyer__number')
    ordering_fields = ('buyer__user__last_name', 'buyer__user__email',
                       'buyer__number', 'seller__user__last_name',
                       'seller__user__email', 'seller__number')
    subscription_features = ('positions',)

    def get_queryset(self):
        company = get_company_from_request(self.request)
        return Position.objects.filter(
            Q(buyer__company=company) |
            Q(seller__company=company)
        ).distinct().order_by('-bought_at', '-pk')

    def destroy(self, request, pk=None):
        """ delete position. but not if is_draft-False"""

        position = self.get_object()
        if position.is_draft is True:
            # update cached shareholder field `order_cache` and cached
            # `share_count` per security and for all securities of the
            # shareholder -> see `None`
            if position.buyer:
                update_order_cache_task.apply_async([position.buyer.pk])
                cache_key = u"shareholder_share_count_{}_{}_{}".format(
                    position.buyer.pk,
                    timezone.now().date().isoformat(),
                    position.security.pk)
                cache.set(cache_key, None)
                cache_key = u"shareholder_share_count_{}_{}_{}".format(
                    position.buyer.pk,
                    timezone.now().date().isoformat(),
                    'None')
                cache.set(cache_key, None)
            if position.seller:
                update_order_cache_task.apply_async([position.seller.pk])
                cache_key = u"shareholder_share_count_{}_{}_{}".format(
                    position.seller.pk,
                    timezone.now().date().isoformat(),
                    position.security.pk)
                cache.set(cache_key, None)
                cache_key = u"shareholder_share_count_{}_{}_{}".format(
                    position.seller.pk,
                    timezone.now().date().isoformat(),
                    'None')
                cache.set(cache_key, None)

            # delete
            position.delete()
            return Response(
                {"success": True}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {
                    'success': False,
                    'errors': [_('Confirmed position cannot be deleted.')]
                },
                status=status.HTTP_400_BAD_REQUEST)

    @detail_route(
        methods=['post'])
    def confirm(self, request, pk=None):
        """ confirm position and make it unchangable """
        position = self.get_object()
        position.is_draft = False
        position.save()
        return Response({"success": True}, status=status.HTTP_200_OK)

    @detail_route(methods=['get'])
    def invalidate(self, request, pk):
        """
        invalidate issued certificate
        """
        position = self.get_object()
        try:
            position.invalidate_certificate()
            return Response(
                PositionSerializer(instance=position,
                                   context={'request': request}).data,
                status=status.HTTP_200_OK)

        except ValueError as e:
            return Response(
                {
                    'success': False,
                    'errors': [_('Position cannot be invalidated. "{}"'
                                 '').format(e)]
                },
                status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['get'])
    def get_new_certificate_id(self, request):
        """
        returns unused new certificate id
        """
        company = get_company_from_request(request)
        cert_id = company.get_new_certificate_id()
        payload = {'certificate_id': cert_id}
        return Response(payload, status=status.HTTP_200_OK)


class OptionPlanViewSet(SubscriptionViewMixin, viewsets.ModelViewSet):
    """ API endpoint to get options """
    serializer_class = OptionPlanSerializer
    permission_classes = [
        IsOperatorPermission,
        HasSubscriptionPermission
    ]
    subscription_features = ('options',)

    def get_queryset(self):
        company = get_company_from_request(self.request)
        return OptionPlan.objects.filter(company=company)

    # FIXME add perms like that to decor. permission_classes=[IsAdminOrIsSelf]
    @detail_route(methods=['post'])
    def upload(self, request, pk=None):
        op = self.get_object()
        # modify data
        serializer = OptionPlanSerializer(data=request.data)
        # add file to serializer
        if serializer.is_valid():
            # FIXME: probably need some validation!
            op.pdf_file = request.FILES['pdf_file']
            op.save()
            op.generate_pdf_file_preview()
            return Response(OptionPlanSerializer(
                op,
                context={'request': request}).data,
                status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)


class OptionTransactionViewSet(SubscriptionViewMixin,
                               viewsets.ModelViewSet):
    """ API endpoint to get options """
    serializer_class = OptionTransactionSerializer
    pagination_class = SmallPagePagination
    permission_classes = [
        IsOperatorPermission,
        HasSubscriptionPermission
    ]
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('buyer__user__first_name', 'buyer__user__last_name',
                     'buyer__user__email', 'seller__user__first_name',
                     'seller__user__last_name', 'seller__user__email',
                     'seller__number', 'buyer__number', 'bought_at',
                     'option_plan__title',
                     'buyer__user__userprofile__company_name',
                     'seller__user__userprofile__company_name',
                     'seller__number', 'buyer__number', 'certificate_id',
                     'stock_book_id')
    ordering_fields = ('buyer__user__last_name', 'buyer__user__email',
                       'buyer__number', 'seller__user__last_name',
                       'seller__user__email', 'seller__number')
    ordering = ('option_plan__pk', '-bought_at')
    subscription_features = ('positions',)

    def get_queryset(self):
        company = get_company_from_request(self.request)
        qs = OptionTransaction.objects.filter(
            option_plan__company=company
        )

        # filter if option plan is given in query params
        # FIXME: why no use filter or detail route???
        pk = self.request.query_params.get('optionplan_pk')
        if pk:
            qs = qs.filter(option_plan_id=pk)

        return qs

    @detail_route(methods=['post'])
    def confirm(self, request, pk=None):
        """ confirm position and make it unchangable """
        position = self.get_object()
        position.is_draft = False
        position.save()
        return Response({"success": True}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        """ delete position. but not if is_draft-False"""
        position = self.get_object()
        if position.is_draft is True:
            # update cached shareholder `field order_cache`
            if position.buyer:
                update_order_cache_task.apply_async([position.buyer.pk])
            if position.seller:
                update_order_cache_task.apply_async([position.seller.pk])
            position.delete()
            return Response(
                {"success": True}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {
                    'success': False,
                    'errors': [_('Confirmed position cannot be deleted.')]
                },
                status=status.HTTP_400_BAD_REQUEST)  # consider 403!


class ReportViewSet(viewsets.ModelViewSet):

    serializer_class = ReportSerializer
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = [
        IsOperatorPermission,
        HasSubscriptionPermission,
    ]
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    filter_fields = ('order_by', 'report_type', 'file_type')
    ordering = ('-pk',)

    def get_queryset(self):
        company = get_company_from_request(self.request)
        qs = Report.objects.filter(
            company=company
        )

        return qs

    def perform_create(self, serializer):
        """ complete missing data for model """
        report = serializer.save(
            eta=timezone.now(),  # placeholder
            user=self.request.user,
            company=get_company_from_request(self.request)
            )
        report.update_eta()
        report.save()
        report.render(notify=True, track_downloads=True)
        return report


class SecurityViewSet(SubscriptionViewMixin, viewsets.ModelViewSet):
    """ API endpoint to get options """
    serializer_class = SecuritySerializer
    permission_classes = [
        IsOperatorPermission,
        HasSubscriptionPermission,
    ]
    subscription_features = ('securities',)

    def get_queryset(self):
        company = get_company_from_request(self.request)
        return Security.objects.filter(company=company)


class ShareholderViewSet(SubscriptionViewMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # FIXME filter by user perms
    serializer_class = ShareholderSerializer
    pagination_class = SmallPagePagination
    permission_classes = [
        IsOperatorPermission,
        HasSubscriptionPermission
    ]
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('user__first_name', 'user__last_name', 'user__email',
                     'number', 'user__userprofile__company_name', 'number')
    ordering_fields = ('user__last_name', 'user__email', 'number',
                       'user__userprofile__company_name')

    subscription_features = ('shareholders',)

    def _filter_queryset_by_order_cache(self, qs):
        """ sort queryset by jsonfield called order_cache on model """
        # FIXME hack, replace once django supports order_by for JSONField
        order_by = self.request.GET.get('ordering')
        if (order_by and 'order_cache' in order_by and '__' in order_by):
            prefix, order_by = self.request.GET.get('ordering').split('__')
            desc = prefix.startswith('-')

            qs = qs.order_by(RawSQL("((order_cache->>%s)::numeric)", (order_by,)))
            if desc:
                qs = qs.reverse()

        return qs

    def get_queryset(self):
        """
        user has no company selected
        """
        self.subscription_features = ['shareholders']

        if not self.request.session.get('company_pk'):
            return Shareholder.objects.none()

        company = get_company_from_request(self.request)

        qs = Shareholder.objects.filter(company=company)
        qs = self._filter_queryset_by_order_cache(qs)
        return qs.select_related('company', 'user', 'user__userprofile') \
            .prefetch_related('user__operator_set') \
            .distinct()

    def get_serializer_class(self):
        if self.action == 'list':
            return ShareholderListSerializer
        # if self.action == 'retrieve':
        #     return ShareholderSerializer
        return ShareholderSerializer

    @detail_route(methods=['get'])
    def number_segments(self, request, pk=None):
        shareholder = self.get_object()
        kwargs = {}

        if request.GET.get('date'):
            # FIXME: parse date(time) properly
            kwargs.update({'date': request.GET.get('date')[:10]})

        data = {}
        for security in shareholder.company.security_set.all():
            if security.track_numbers:
                kwargs.update({'security': security})
                data.update({
                    security.pk: shareholder.current_segments(**kwargs)
                })
        return Response(data, status=status.HTTP_200_OK)

    @list_route(methods=['get'])
    def company_number_segments(self, request):
        company = get_company_from_request(request)
        shareholder = company.get_company_shareholder()
        kwargs = {}

        if request.GET.get('date'):
            # FIXME: parse date(time) properly
            kwargs.update({'date': request.GET.get('date')[:10]})

        data = {}
        for security in shareholder.company.security_set.all():
            if security.track_numbers:
                kwargs.update({'security': security})
                data.update({
                    security.pk: shareholder.current_segments(**kwargs)
                })
        return Response(data, status=status.HTTP_200_OK)

    @list_route(methods=['get'])
    def option_holder(self, request):
        """
        returns the captable part for all option holders
        """
        self.subscription_features = ['shareholders', 'options']

        # if user has no company yet
        if not self.request.session.get('company_pk'):
            return Response(Shareholder.objects.none())

        company = get_company_from_request(request)
        ohs = company.get_active_option_holders()

        ohs = self.filter_queryset(ohs)
        page = self.paginate_queryset(ohs)
        if page is not None:
            serializer = OptionHolderSerializer(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = OptionHolderSerializer(
            ohs, many=True, context={'request': request})
        return Response(serializer.data)

    @list_route(methods=['get'])
    def get_new_shareholder_number(self, request):
        """
        returns unused new unused shareholder number
        """
        company = get_company_from_request(request)
        number = company.get_new_shareholder_number()
        payload = {'number': number}
        return Response(payload, status=status.HTTP_200_OK)


# --- VIEWS

class AddCompanyView(APIView):
    """ view to initially setup a company """

    queryset = Company.objects.none()
    permission_classes = [
        UserCanAddCompanyPermission,
    ]

    def post(self, request, format=None):
        serializer = AddCompanySerializer(data=request.data,
                                          context={'request': self.request})
        if serializer.is_valid() and request.user.is_authenticated():
            company = serializer.save(user=request.user)
            # once user added a company save it to the session to allow
            # multi company handling for single user
            request.session['company_pk'] = company.pk
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddShareSplit(APIView):
    """ creates a share split. danger: can be set to be in the past and ALL
    following transactions must be adjusted
    """
    permission_classes = [
        IsOperatorPermission,
        HasSubscriptionPermission,
    ]
    subscription_features = ('positions',)

    def _validate_data(self, data):
        errors = {}
        if not data.get('execute_at'):
            errors.update({'execute_at': [_('Field may not be empty.')]})
        if not data.get('dividend'):
            errors.update({'dividend': [_('Field may not be empty.')]})
        if not data.get('divisor'):
            errors.update({'divisor': [_('Field may not be empty.')]})
        if not data.get('security'):
            errors.update({'security': [_('Field may not be empty.')]})

        if not errors:
            return True, {}
        else:
            return False, errors

    def post(self, request, fomat=None):
        data = request.data
        is_valid, errors = self._validate_data(data)
        if is_valid:
            # get company and run company.split_shares(data)
            company = get_company_from_request(request)
            data.update({
                'execute_at': dateutil.parser.parse(data['execute_at']),
                'security': Security.objects.get(id=data['security']['pk'])
            })
            company.split_shares(data)

            positions = Position.objects.filter(
                buyer__company__operator__user=request.user).order_by(
                    '-bought_at')

            serializer = PositionSerializer(
                positions, many=True, context={'request': request})
            return Response(
                {'success': True, 'data': serializer.data},
                status=status.HTTP_201_CREATED)

        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class AvailableOptionSegmentsView(APIView):

    permission_classes = [
        IsOperatorPermission,
        HasSubscriptionPermission,
    ]

    def get(self, request, optionsplan_id, shareholder_id):
        """
        returns available option segments from shareholder X and
        optionplan Y
        """
        company = get_company_from_request(request)
        optionplan = get_object_or_404(OptionPlan.objects.filter(
            company=company), pk=optionsplan_id)
        shareholder = get_object_or_404(Shareholder.objects.filter(
            company=company), pk=shareholder_id)

        kwargs = {
            'security': optionplan.security,
            'optionplan': optionplan,
        }

        if request.GET.get('date'):
            kwargs.update({'date': request.GET.get('date')[:10]})

        return Response(shareholder.current_options_segments(**kwargs))


class BankView(ListAPIView):
    """
    endpoint for bank search
    """
    permission_classes = (IsOperatorPermission, HasSubscriptionPermission)
    serializer_class = BankSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'short_name', 'swift', 'city')
    ordering = ('name',)
    queryset = Bank.objects.all()


class LanguageView(APIView):
    """
    Endpint delivering language options
    """
    permission_classes = (AllowAny,)

    def get(self, *args, **kwargs):
        from django_languages.languages import LANGUAGES
        languages = []
        for language in LANGUAGES:
            languages.append({
                'iso': language[0],
                'name': language[1],
            })
        return Response(languages)


class UserViewSet(viewsets.ModelViewSet):
    """ API endpoint to get user base info """
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(id=user.id)


class CountryViewSet(viewsets.ModelViewSet):
    """ API endpoint to get user base info """
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    permission_classes = [
        IsAuthenticated
    ]


class InviteeUpdateView(APIView):
    """ API endpoint to get user base info """
    permission_classes = (AllowAny,)

    def post(self, request, format=None):

        serializer = UserWithEmailOnlySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(username=serializer.validated_data['email'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
