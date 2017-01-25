from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.template import RequestContext, loader
from django.utils.translation import ugettext as _
from django.views.generic import DetailView
from sendfile import sendfile

from project.permissions import OperatorPermissionRequiredMixin
from shareholder.models import (OptionPlan, OptionTransaction, Position,
                                Shareholder)
from utils.formatters import human_readable_segments


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
            sec.options_count = shareholder.options_count(security=sec) or 0

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

