import dateutil.parser
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from rest_framework import status, viewsets
from rest_framework.decorators import detail_route, list_route
from services.rest.pagination import SmallPagePagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters

from services.rest.permissions import (SafeMethodsOnlyPermission,
                                       UserCanAddCompanyPermission,
                                       UserIsOperatorPermission)
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
from utils.session import get_company_from_request

User = get_user_model()


# --- VIEWSETS

class ShareholderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # FIXME filter by user perms
    serializer_class = ShareholderSerializer
    pagination_class = SmallPagePagination
    permission_classes = [
        UserIsOperatorPermission,
    ]
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('user__first_name', 'user__last_name', 'user__email',
                     'number', 'user__userprofile__company_name', 'number')
    ordering_fields = ('user__last_name', 'user__email', 'number')

    def get_object(self):
        try:
            return Shareholder.objects.get(pk=self.kwargs.get('pk'))
        except Shareholder.DoesNotExist:
            raise Http404

    def get_queryset(self):
        """
        user has no company selected
        """
        if not self.request.session.get('company_pk'):
            return Shareholder.objects.none()

        company = get_company_from_request(self.request)

        return Shareholder.objects.filter(company=company)\
            .select_related('company', 'user', 'user__userprofile') \
            .prefetch_related('user__operator_set') \
            .distinct()

    def get_serializer_class(self):
        if self.action == 'list':
            return ShareholderListSerializer
        if self.action == 'retrieve':
            return ShareholderSerializer
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
        company = get_company_from_request(request)
        shareholder = company.get_company_shareholder()
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
        # if user has no company yet
        if not self.request.session.get('company_pk'):
            return Response(Shareholder.objects.none())

        company = Company.objects.get(pk=self.request.session.get('company_pk'))

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


class OperatorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # FIXME filter by user perms
    serializer_class = OperatorSerializer
    permission_classes = [
        UserIsOperatorPermission,
    ]

    def get_object(self, pk):
        try:
            return Operator.objects.get(pk=pk)
        except Operator.DoesNotExist:
            raise Http404

    def get_queryset(self):
        company = get_company_from_request(self.request)
        return Operator.objects.filter(company=company)\
            .distinct()

    def destroy(self, request, pk=None):
        operator = self.get_object(pk)
        company_ids = request.user.operator_set.all().values_list(
            'company__id', flat=True).distinct()
        # cannot remove himself
        if operator not in request.user.operator_set.all():
            # user can only edit corps he manages
            if operator.company.id in company_ids:
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
        UserIsOperatorPermission,
    ]
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('user__first_name', 'user__last_name', 'user__email',
                     'number')
    ordering_fields = ('user__last_name', 'user__email', 'number')

    def get_queryset(self):
        user = self.request.user
        return Company.objects.filter(operator__user=user)

    # FIXME add perms like that to decor. permission_classes=[IsAdminOrIsSelf]
    @detail_route(methods=['post'])
    def upload(self, request, pk=None):
        obj = self.get_object()
        obj.logo = request.FILES['logo']
        obj.save()
        return Response(CompanySerializer(
            obj,
            context={'request': request}).data,
            status=status.HTTP_201_CREATED)


# --- VIEWS

class AddCompanyView(APIView):
    """ view to initially setup a company """

    queryset = Company.objects.none()
    permission_classes = [
        UserCanAddCompanyPermission,
    ]

    def post(self, request, format=None):
        serializer = AddCompanySerializer(data=request.data)
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
        UserCanAddCompanyPermission,
    ]

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

    permission_classes = [UserIsOperatorPermission]

    def get(self, request, optionsplan_id, shareholder_id):
        """
        returns available option segments from shareholder X and
        optionplan Y
        """
        optionplan = get_object_or_404(OptionPlan, pk=optionsplan_id)
        shareholder = get_object_or_404(Shareholder, pk=shareholder_id)

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


class UserViewSet(viewsets.ModelViewSet):
    """ API endpoint to get user base info """
    serializer_class = UserSerializer
    permission_classes = [
        SafeMethodsOnlyPermission,
    ]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(id=user.id)


class CountryViewSet(viewsets.ModelViewSet):
    """ API endpoint to get user base info """
    serializer_class = CountrySerializer
    permission_classes = [
        SafeMethodsOnlyPermission,
    ]

    def get_queryset(self):
        countries = Country.objects.all()
        return countries


class InviteeUpdateView(APIView):
    """ API endpoint to get user base info """
    permission_classes = (AllowAny,)

    def post(self, request, format=None):

        serializer = UserWithEmailOnlySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(username=serializer.validated_data['email'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PositionViewSet(viewsets.ModelViewSet):
    """ API endpoint to get positions """
    serializer_class = PositionSerializer
    pagination_class = SmallPagePagination
    permission_classes = [
        UserIsOperatorPermission,
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

    def get_queryset(self):
        company = get_company_from_request(self.request)
        return Position.objects.filter(
            Q(buyer__company=company) |
            Q(seller__company=company)
        ).distinct().order_by('-bought_at', '-pk')

    @detail_route(
        methods=['post'], permission_classes=[UserIsOperatorPermission])
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


class SecurityViewSet(viewsets.ModelViewSet):
    """ API endpoint to get options """
    serializer_class = SecuritySerializer
    permission_classes = [
        UserIsOperatorPermission,
    ]

    def get_queryset(self):
        company = get_company_from_request(self.request)
        return Security.objects.filter(company=company)


class OptionPlanViewSet(viewsets.ModelViewSet):
    """ API endpoint to get options """
    serializer_class = OptionPlanSerializer
    permission_classes = [
        # UserCanAddOptionPlanPermission,
    ]

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


class OptionTransactionViewSet(viewsets.ModelViewSet):
    """ API endpoint to get options """
    serializer_class = OptionTransactionSerializer
    pagination_class = SmallPagePagination
    permission_classes = [
        UserIsOperatorPermission
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

    def get_queryset(self):
        company = get_company_from_request(self.request)
        qs = OptionTransaction.objects.filter(
            option_plan__company=company
        )

        # filter if option plan is given in query params
        if self.request.query_params.get('optionplan_pk', None):
            qs = qs.filter(
                option_plan__pk=self.request.query_params.get('optionplan_pk'))

        return qs

    @detail_route(
        methods=['post'], permission_classes=[UserIsOperatorPermission])
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
