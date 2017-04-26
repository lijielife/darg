import os

from django.contrib.auth.decorators import login_required
from django.core import signing
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.template import loader
from django.utils.timezone import now
from django.utils.translation import ugettext as _
from django.views.generic import DetailView, ListView
from sendfile import sendfile

from company.mixins import SubscriptionViewMixin
from project.permissions import OperatorPermissionRequiredMixin
from shareholder.models import (OptionPlan, OptionTransaction, Position,
                                Shareholder, ShareholderStatement)
from utils.formatters import human_readable_segments

from .mixins import (AuthTokenSingleViewMixin,
                     ShareholderStatementReportViewMixin)


@login_required
def positions(request):
    template = loader.get_template('positions.html')
    return HttpResponse(template.render(request=request))


@login_required
def options(request):
    template = loader.get_template('options.html')
    return HttpResponse(template.render(request=request))


class OptionTransactionView(OperatorPermissionRequiredMixin, DetailView):
    """
    shows details for one shareholder
    """
    model = OptionTransaction
    context_object_name = 'optiontransaction'


class PositionView(OperatorPermissionRequiredMixin, DetailView):
    """
    shows details for one shareholder
    """
    model = Position
    context_object_name = 'position'


class ShareholderView(OperatorPermissionRequiredMixin, DetailView):
    """
    shows details for one shareholder
    """
    model = Shareholder
    context_object_name = 'shareholder'

    def get_context_data(self, *args, **kwargs):
        context = super(ShareholderView, self).get_context_data(
            *args, **kwargs)

        shareholder = self.get_object()
        securities = shareholder.company.security_set.all()

        # hack security props for shareholder spec data
        for sec in securities:
            if sec.track_numbers:
                if shareholder.current_segments(sec):
                    sec.segments = human_readable_segments(
                        shareholder.current_segments(sec))
            sec.count = shareholder.share_count(security=sec) or 0
            sec.options_count = shareholder.options_count(security=sec) or 0

        context.update({
            'securities': securities})

        return context


@login_required
def optionsplan(request, optionsplan_id):
    template = loader.get_template('optionsplan.html')
    optionsplan = get_object_or_404(OptionPlan, id=int(optionsplan_id))
    context = {"optionplan": optionsplan, 'request': request}
    return HttpResponse(template.render(context=context, request=request))


@login_required
def optionsplan_download_pdf(request, optionsplan_id):
    optionplan = OptionPlan.objects.get(id=optionsplan_id)
    if optionplan.company.operator_set.filter(user=request.user).exists():
        return sendfile(request, optionplan.pdf_file.path)
    else:
        return HttpResponseForbidden(_("Permission denied"))


@login_required
def optionsplan_download_img(request, optionsplan_id):
    optionplan = OptionPlan.objects.get(id=optionsplan_id)
    if optionplan.company.operator_set.filter(user=request.user).exists():
        return sendfile(request, optionplan.pdf_file_preview_path())
    else:
        return HttpResponseForbidden(_("Permission denied"))


class StatementListView(ListView):

    template_name = 'statement_list.html'  # in shareholder/templates
    allow_empty = False

    def get_queryset(self):
        qs = ShareholderStatement.objects.filter(user=self.request.user)
        return qs.order_by('report_id')


statement_list = login_required(StatementListView.as_view())


class StatementDownloadPDFView(AuthTokenSingleViewMixin, DetailView):

    http_method_names = ['get']
    login_required = True  # see AuthTokenViewMixin
    model = ShareholderStatement

    def raise_404_error(self, message=None):
        if message is None:
            message = (_("No %(verbose_name)s found matching the query") %
                       {'verbose_name': self.model._meta.verbose_name})
        raise Http404(message)

    def get_queryset(self):
        # TODO: consider admin/superusers
        user = self.request.user
        shareholder_statements = user.shareholderstatement_set.all()
        operator_statements = ShareholderStatement.objects.filter(
            report__company__operator__user=user)
        return shareholder_statements | operator_statements

    def get_object(self, queryset=None):

        if queryset is None:
            queryset = self.get_queryset()

        file_hash = self.request.GET.get('file', '')
        salt = getattr(self.model, 'SIGNING_SALT', '')
        try:
            data = signing.loads(file_hash, salt=salt)
        except signing.BadSignature:
            # FIXME: should we reveal that hash is invalid?
            self.raise_404_error()

        queryset = queryset.filter(pk=data.get('pk'))

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            self.raise_404_error('obj not found')

        # check all stored parameters in data
        operators_pks = obj.report.company.operator_set.all().values_list(
            'user__pk', flat=True)
        if not data.get('company_pk') == obj.report.company_id:
            self.raise_404_error('company mismatch')
        elif not data.get('date') == str(obj.report.report_date):
            self.raise_404_error('date mismatch')
        elif (data.get('user_pk') != obj.user_id and
              self.request.user.pk not in operators_pks and
              self.request.user.is_superuser is not True):
            self.raise_404_error('user mismatch')

        return obj

    def get(self, request, *args, **kwargs):

        self.object = self.get_object()

        if not os.path.isfile(self.object.pdf_file):
            # TODO: how to handle this without outraging the user?
            self.raise_404_error()

        # try:
        #     with open(self.object.pdf_file, 'r') as f:
        #         content = f.read()
        # except:
        #     # TODO: proper error handling
        #     # raise Http404(_('We could not read this file.'))
        #     self.raise_404_error()

        # set download date
        self.object.pdf_downloaded_at = now()
        self.object.save()

        # return FileResponse(content, content_type='application/pdf')
        return sendfile(request, self.object.pdf_file)


statement_download_pdf = StatementDownloadPDFView.as_view()


class StatementReportListView(ShareholderStatementReportViewMixin,
                              SubscriptionViewMixin, ListView):

    template_name = 'statement_report_list.html'  # in shareholder/templates
    allow_empty = False


statement_report_list = login_required(StatementReportListView.as_view())


class StatementReportDetailView(ShareholderStatementReportViewMixin,
                                SubscriptionViewMixin, DetailView):

    template_name = 'statement_report_detail.html'  # in shareholder/templates


statement_report_detail = login_required(StatementReportDetailView.as_view())
