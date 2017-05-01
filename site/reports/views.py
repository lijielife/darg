from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView
from django.utils import timezone
from sendfile import sendfile

from reports.models import Report
from utils.session import get_company_from_request


@login_required
def report_download(request, report_id):
    """ check for user is operator and send download of report file """
    report = get_object_or_404(Report, id=report_id)
    if report.company.operator_set.filter(user=request.user).exists():
        if not report.downloaded_at:
            report.downloaded_at = timezone.now()
            report.save()
        return sendfile(request, report.file.path, attachment=True,
                        attachment_filename=report.get_filename())
    else:
        return HttpResponseForbidden(_("Permission denied"))


class IndexView(TemplateView):

    template_name = 'reports/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['company'] = get_company_from_request(self.request)
        return context
