import dateutil.parser
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from rest_framework import status, viewsets
from rest_framework.decorators import detail_route, list_route
from services.rest.pagination import SmallPagePagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters

from company.mixins import SubscriptionViewMixin
from services.rest.permissions import (IsOperatorPermission,
                                       HasSubscriptionPermission)
from services.rest.serializers import (AddCompanySerializer, CompanySerializer,
                                       CountrySerializer, OperatorSerializer,
                                       OptionHolderSerializer,
                                       OptionPlanSerializer,
                                       OptionTransactionSerializer,
                                       PositionSerializer, SecuritySerializer,
                                       ShareholderSerializer, UserSerializer,
                                       UserWithEmailOnlySerializer,
                                       ShareholderListSerializer)
from shareholder.models import (Company, Country, Operator, OptionPlan,
                                OptionTransaction, Position, Security,
                                Shareholder)


User = get_user_model()


# --- VIEWSETS

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
    ordering_fields = ('user__last_name', 'user__email', 'number')

    subscription_features = ('shareholders',)

    def get_user_companies(self):
        return Company.objects.filter(operator__user=self.request.user)

    def get_object(self):
        # try:
        #     return self.get_queryset().get(pk=self.kwargs.get('pk'))
        # except Shareholder.DoesNotExist:
        #     raise Http404
        qs = self.get_queryset()
        print(qs.values_list('pk', flat=True), self.kwargs.get('pk'))
        return super(ShareholderViewSet, self).get_object()

    def get_queryset(self):
        self.subscription_features = ['shareholders']
        qs = Shareholder.objects.filter(company_id__in=self.get_company_pks())
        return (qs.select_related('company', 'user', 'user__userprofile')
                .prefetch_related('user__operator_set')
                .distinct())

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
        operator = request.user.operator_set.first()  # FIXME
        shareholder = operator.company.get_company_shareholder()
        kwargs = {}

        if request.GET.get('date'):
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
    def option_holder(self, request, pk=None):
        """
        returns the captable part for all option holders
        """
        self.subscription_features = ['shareholders', 'options']
        ohs = Shareholder.objects.none()
        for company in Company.objects.filter(pk__in=self.get_company_pks()):
            ohs |= company.get_active_option_holders()

        ohs = self.filter_queryset(ohs)
        page = self.paginate_queryset(ohs)
        if page is not None:
            serializer = OptionHolderSerializer(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = OptionHolderSerializer(
            ohs, many=True, context={'request': request})
        return Response(serializer.data)


class OperatorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # FIXME filter by user perms
    serializer_class = OperatorSerializer
    permission_classes = [
        IsOperatorPermission
    ]
    queryset = Operator.objects.none()

    def get_queryset(self):
        return Operator.objects.filter(
            company__operator__user=self.request.user).distinct()

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


class CompanyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # FIXME filter by user perms
    queryset = Company.objects.all()
    pagination_class = SmallPagePagination
    serializer_class = CompanySerializer
    permission_classes = [
        IsOperatorPermission
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


# --- VIEWS

class AddCompanyView(APIView):
    """ view to initially setup a company """

    # queryset = Company.objects.none()
    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request, format=None):
        serializer = AddCompanySerializer(data=request.data)
        if serializer.is_valid() and request.user.is_authenticated():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddShareSplit(SubscriptionViewMixin, APIView):
    """ creates a share split. danger: can be set to be in the past and ALL
    following transactions must be adjusted
    """
    permission_classes = [
        IsOperatorPermission,
        HasSubscriptionPermission
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
            # FIXME
            company = request.user.operator_set.earliest('id').company
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
        IsOperatorPermission
    ]

    def get_user_companies(self):
        return Company.objects.filter(operator__user=self.request.user)

    def get(self, request, optionsplan_id, shareholder_id):
        """
        returns available option segments from shareholder X and
        optionplan Y
        """
        user_companies = self.get_user_companies()
        optionplan = get_object_or_404(OptionPlan, pk=optionsplan_id,
                                       company__in=user_companies)
        shareholder = get_object_or_404(Shareholder, pk=shareholder_id,
                                        # company__in=user_companies)
                                        company=optionplan.company)

        # FIXME: subscription check required?

        kwargs = {
            'security': optionplan.security,
            'optionplan': optionplan,
        }

        if request.GET.get('date'):
            kwargs.update({'date': request.GET.get('date')[:10]})

        return Response(shareholder.current_options_segments(**kwargs))


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


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """ API endpoint to get user base info """
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.pk)


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    """ API endpoint to get user base info """
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    permission_classes = [
        IsAuthenticated
    ]


class InviteeUpdateView(APIView):
    """ API endpoint to get user base info """
    permission_classes = [
        AllowAny
    ]

    def post(self, request, format=None):
        serializer = UserWithEmailOnlySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(username=serializer.validated_data['email'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

    def get_user_companies(self):
        return Company.objects.filter(operator__user=self.request.user)

    def get_queryset(self):
        company_pks = self.get_company_pks()
        return Position.objects.filter(
            Q(buyer__company_id__in=company_pks) |
            Q(seller__company_id__in=company_pks)
        ).distinct().order_by('-bought_at', '-pk')

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


class SecurityViewSet(SubscriptionViewMixin, viewsets.ModelViewSet):
    """ API endpoint to get options """
    serializer_class = SecuritySerializer
    permission_classes = [
        IsOperatorPermission,
        HasSubscriptionPermission
    ]
    subscription_features = ('securities',)

    def get_user_companies(self):
        return Company.objects.filter(operator__user=self.request.user)

    def get_queryset(self):
        return Security.objects.filter(company_id__in=self.get_company_pks())


class OptionPlanViewSet(SubscriptionViewMixin, viewsets.ModelViewSet):
    """ API endpoint to get options """
    serializer_class = OptionPlanSerializer
    permission_classes = [
        IsOperatorPermission,
        HasSubscriptionPermission
    ]
    subscription_features = ('options',)

    def get_user_companies(self):
        return Company.objects.filter(operator__user=self.request.user)

    def get_queryset(self):
        return OptionPlan.objects.filter(company_id__in=self.get_company_pks())

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

    def get_user_companies(self):
        return Company.objects.filter(operator__user=self.request.user)

    def get_queryset(self):
        qs = OptionTransaction.objects.filter(
            option_plan__company_id__in=self.get_company_pks()
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
