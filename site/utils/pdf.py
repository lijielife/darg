import os

import cStringIO as StringIO
from xhtml2pdf import pisa

from django.conf import settings
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import escape


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(
        StringIO.StringIO(html.encode("UTF-8")),
        result,
        link_callback=fetch_resources,
        encoding='UTF-8')
    if not pdf.err:
        return result.getvalue()

    raise ValueError('We had some errors<pre>%s</pre>' % escape(html))


def render_to_pdf_response(template_src, context_dict):
    content = render_to_pdf(template_src, context_dict)
    return HttpResponse(content, content_type='application/pdf')


def fetch_resources(uri, rel):
    path = os.path.join(
        settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))

    return path
