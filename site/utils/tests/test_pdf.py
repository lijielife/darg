
from django.conf import settings
from django.template import Template, Context
from django.test import TestCase

import mock

from ..pdf import (fetch_resources, render_pdf, render_to_pdf,
                   render_to_pdf_response)


class PdfUtilsTestCase(TestCase):

    def test_fetch_resources(self):

        # pass
        uri = 'foo/bar'
        path = fetch_resources(uri, None)
        self.assertEqual(path, uri)

        # MEDIA_URL
        uri = settings.MEDIA_URL + 'test/me'
        path = fetch_resources(uri, None)
        self.assertTrue(path.startswith(settings.MEDIA_ROOT))

        # STATIC_URL
        uri = settings.STATIC_URL + 'test/me'
        path = fetch_resources(uri, None)
        self.assertTrue(path.startswith(settings.STATIC_ROOT))

    def test_render_pdf(self):
        html = '<foo>bar</foo>'
        pdf = render_pdf(html)
        self.assertTrue(pdf)

        with mock.patch('xhtml2pdf.pisa.pisaDocument') as mock_pisa_document:
            with self.assertRaises(ValueError):
                pdf = render_pdf(html)

            mock_pisa_document.assert_called()

    @mock.patch('utils.pdf.get_template')
    @mock.patch('utils.pdf.render_pdf')
    def test_render_to_pdf(self, mock_render_pdf, mock_get_template):

        template_str = '<foo>{{ bar }}</foo>'
        template = Template(template_str)
        mock_get_template.return_value = template

        context = dict(bar='bar')
        render_to_pdf('foo.html', context)
        mock_get_template.assert_called()
        mock_render_pdf.assert_called_with(template.render(Context(context)))

    @mock.patch('utils.pdf.render_to_pdf')
    def test_render_to_pdf_response(self, mock_render_to_pdf):
        mock_render_to_pdf.return_value = 'PDFCONTENT'
        res = render_to_pdf_response('foo.html', dict())
        self.assertEqual(res.status_code, 200)
        self.assertIn('PDFCONTENT', res.content)
