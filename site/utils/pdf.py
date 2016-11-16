import os

import cStringIO as StringIO
from xhtml2pdf import pisa

from django.conf import settings
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import escape


def fetch_resources(uri, rel):
    path = os.path.join(
        settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))

    return path


def render_pdf(html):
    """
    render html to pdf (returns None if any errors occur)
    """
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(
        StringIO.StringIO(html.encode("UTF-8")),
        result,
        link_callback=fetch_resources,
        encoding='UTF-8')

    if pdf.err:
        return

    return result


def render_to_pdf_response(template_src, context_dict):
    """
    render a pdf and return as HttpResponse
    """
    template = get_template(template_src)
    html = template.render(Context(context_dict))
    pdf = render_to_pdf(template_src, context_dict)
    if not pdf:
        return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
    return HttpResponse(pdf.getvalue(), content_type='application/pdf')


def render_to_pdf(template_src, context_dict):
    """
    this method is named a bit misleading as it actually returns a HttpResponse
    instead of a suggested pdf (use render_to_pdf_response instead)
    """
    return render_to_pdf_response(template_src, context_dict)
