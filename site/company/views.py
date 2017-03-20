from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from shareholder.models import Company, Operator


@login_required
def company(request, company_id):
    """
    show company detail page
    """
    template = loader.get_template('company.html')
    company = get_object_or_404(Company, id=int(company_id))
    context = RequestContext(request, {'company': company})
    return HttpResponse(template.render(context))


@login_required
def company_select(request):
    """
    view to select company to work within for operators
    """
    template = loader.get_template('company_select.html')
    context = RequestContext(request)

    # company choice: set to session and redirect to start...
    company_id = int(request.GET.get('company_id', 0))
    if company_id:
        operator = get_object_or_404(Operator, company__pk=company_id,
                                     user=request.user)
        request.session['company_pk'] = operator.company.pk
        return redirect("start")

    # add new corp, clean session and redirect to start...
    if request.GET.get('add_company'):
        if request.session.get('company_pk'):
            del request.session['company_pk']
        return redirect("start")

    # render company choice view
    return HttpResponse(template.render(context))
