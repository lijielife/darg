from django.views.generic import TemplateView
from utils.session import get_company_from_request


class IndexView(TemplateView):

    template_name = 'reports/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['company'] = get_company_from_request(self.request)
        return context
