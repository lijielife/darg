import os

import cStringIO as StringIO
from xhtml2pdf import pisa

from django.conf import settings
from django.contrib.staticfiles import finders
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import escape


def fetch_resources(uri, rel):
    if uri.startswith(settings.MEDIA_URL):
        filepath = uri.split(settings.MEDIA_URL, 1)[1]
        path = os.path.join(settings.MEDIA_ROOT, filepath)
    elif uri.startswith(settings.STATIC_URL):
        filepath = uri.split(settings.STATIC_URL, 1)[1]
        path = finders.find(filepath)
        if path is None:
            # maybe we get lucky
            path = os.path.join(settings.STATIC_ROOT, filepath)
    else:
        # pass
        path = uri
    return path


def render_pdf(html):
    """
    render html to pdf (raises ValueError if any errors occur)
    """
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(
        StringIO.StringIO(html.encode("UTF-8")),
        result,
        link_callback=fetch_resources,
        encoding='UTF-8')

    if not pdf.err:
        return result.getvalue()

    raise ValueError('We had some errors<pre>%s</pre>' % escape(html))


def render_to_pdf(template_src, context_dict):
    """
    renders html template with context to pdf
    """
    template = get_template(template_src)
    html = template.render(Context(context_dict))
    return render_pdf(html)


def render_to_pdf_response(template_src, context_dict):
    """
    render a pdf and return as HttpResponse
    """
    content = render_to_pdf(template_src, context_dict)
    return HttpResponse(content, content_type='application/pdf')
