
import os

from django.http import HttpResponse, Http404, FileResponse
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils.timezone import now
from django.utils.translation import ugettext as _
from django.views.generic import ListView, DetailView

from sendfile import sendfile

from shareholder.models import (Shareholder, OptionPlan, ShareholderStatement,
                                ShareholderStatementReport)
from project.permissions import OperatorPermissionRequiredMixin
from utils.formatters import human_readable_segments

from .mixins import AuthTokenSingleViewMixin


@login_required
def positions(request):
    template = loader.get_template('positions.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))


@login_required
def options(request):
    template = loader.get_template('options.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))


class ShareholderView(OperatorPermissionRequiredMixin, DetailView):
    """
    shows details for one shareholder
    """
    model = Shareholder
    context_object_name = 'shareholder'

    def get_context_data(self, *args, **kwargs):
        context = super(ShareholderView, self).get_context_data(*args, **kwargs)

        shareholder = self.get_object()
        securities = shareholder.company.security_set.all()

        # hack security props for shareholder spec data
        for sec in securities:
            if sec.track_numbers:
                if shareholder.current_segments(sec):
                    sec.segments = human_readable_segments(
                        shareholder.current_segments(sec))
            sec.count = shareholder.share_count(security=sec) or 0

        context.update({
            'securities': securities})

        return context


@login_required
def optionsplan(request, optionsplan_id):
    template = loader.get_template('optionsplan.html')
    optionsplan = get_object_or_404(OptionPlan, id=int(optionsplan_id))
    context = RequestContext(request, {"optionplan": optionsplan})
    return HttpResponse(template.render(context))


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

    def get_queryset(self):
        qs = ShareholderStatement.objects.filter(user=self.request.user)
        return qs.order_by('report_id')


statement_list = login_required(StatementListView.as_view())


class StatementDownloadPDFView(AuthTokenSingleViewMixin, DetailView):

    http_method_names = ['get']
    login_required = True  # see AuthTokenViewMixin

    def get_queryset(self):
        return self.request.user.shareholderstatement_set.all()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not os.path.isfile(self.object.pdf_file):
            # TODO: how to handle this without outraging the user?
            raise Http404(_('We could not find this file.'))

        try:
            with open(self.object.pdf_file, 'r') as f:
                content = f.read()
        except:
            # TODO: proper error handling
            raise Http404(_('We could not read this file.'))

        # set download date
        self.object.pdf_downloaded_at = now()
        self.object.save()

        return FileResponse(content, content_type='application/pdf')


statement_download_pdf = StatementDownloadPDFView.as_view()


class StatementReportListView(ListView):

    template_name = 'statement_report_list.html'  # in shareholder/templates
    allow_empty = False

    def get_queryset(self):
        company_ids = self.request.user.operator_set.values_list(
            'company_id', flat=True)
        qs = ShareholderStatementReport.objects.filter(company__in=company_ids)
        return qs.order_by('company__name')

statement_report_list = login_required(StatementReportListView.as_view())


class StatementReportDetailView(DetailView):

    template_name = 'statement_report_detail.html'  # in shareholder/templates

    def get_queryset(self):
        company_ids = self.request.user.operator_set.values_list(
            'company_id', flat=True)
        qs = ShareholderStatementReport.objects.filter(company__in=company_ids)
        return qs

statement_report_detail = login_required(StatementReportDetailView.as_view())
