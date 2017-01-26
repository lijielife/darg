from django.views.generic import TemplateView


class IndexView(TemplateView):

    template_name = 'reports/index.html'
