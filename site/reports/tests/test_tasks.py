#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import logging
from decimal import Decimal

from django.core import mail
from django.template.defaultfilters import slugify
from django.test import TestCase
from django.utils import timezone
from mock import patch
from model_mommy import mommy

from project.generators import (CompanyGenerator,
                                ComplexShareholderConstellationGenerator,
                                PositionGenerator, ReportGenerator)
from project.tests.mixins import MoreAssertsTestCaseMixin
from reports.tasks import (_add_file_to_report, _collect_csv_data,
                           _collect_participation_csv_data,
                           _get_address_data_pdf_context,
                           _get_assembly_participation_pdf_context,
                           _get_captable_pdf_context,
                           _get_certificates_pdf_context, _get_contacts,
                           _get_default_pdf_context, _get_filename,
                           _get_vested_shares_pdf_context, _order_queryset,
                           _parse_ordering, _prepare_report, _send_notify,
                           _summarize_report, prerender_reports,
                           render_address_data_pdf, render_address_data_xls,
                           render_assembly_participation_pdf,
                           render_assembly_participation_xls,
                           render_captable_pdf, render_captable_xls,
                           render_certificates_pdf, render_certificates_xls,
                           render_vested_shares_pdf, render_vested_shares_xls)
from shareholder.models import Shareholder


logger = logging.getLogger(__name__)


# --- TASKS
class ReportTaskTestCase(MoreAssertsTestCaseMixin, TestCase):

    def setUp(self):
        self.shs, self.sec = (
            ComplexShareholderConstellationGenerator().generate())
        self.company = self.shs[0].company
        # have at least one unicode sh number (failed on test prev.)
        sh = self.shs[0]
        sh.number = u'999ü'
        sh.save()

    def test_get_certificates_pdf_context(self):
        """ get context for certificate report pdf """
        pos = self.company.shareholder_set.first().buyer.first()
        pos.certificate_id = 99
        pos.printed_at = timezone.now().date()
        pos.save()
        res = _get_certificates_pdf_context(self.company, timezone.now().date())
        self.assertEqual(
            res.keys(), ['pagesize', 'table_data', 'company', 'currency',
                         'header', 'report_date', 'heading', 'today'])
        self.assertEqual(len(res['table_data']), 1)

    def test_collect_csv_data(self):
        """ render csv date for xls/csv export """
        row = _collect_csv_data(self.shs[1], timezone.now().date())
        # required to write proper number formats in xlsx
        for x in [22, 23, 24, 16]:
            self.assertTrue(isinstance(row[0][x], (float, int, Decimal)))

    def test_collect_participation_csv_data(self):
        """ return single row for csv file """
        res = _collect_participation_csv_data(self.shs[0],
                                              timezone.now().date())
        self.assertEqual(len(res[0]), 9)
        self.assertEqual(res[0][0], self.shs[0].number)

    def test_get_address_data_pdf_context(self):
        """ get context for address data pdf  """
        res = _get_address_data_pdf_context(self.company, timezone.now().date())
        self.assertEqual(res.keys(), ['pagesize', 'table_data', 'company',
                                      'currency', 'header', 'report_date',
                                      'heading', 'today'])
        self.assertEqual(len(res['table_data']), 11)

    def test_get_assembly_participation_pdf_context(self):
        res = _get_assembly_participation_pdf_context(
            self.shs[0].company, date=timezone.now().date())
        self.assertEqual(res.keys(), ['pagesize', 'table_data', 'company',
                                      'currency', 'header', 'report_date',
                                      'heading', 'today'])
        self.assertEqual(len(res['table_data']), 11)

    def test_get_captable_pdf_context(self):

        res = _get_captable_pdf_context(self.shs[0].company,
                                        ordering='-share_count',
                                        date=timezone.now().date())
        self.assertEqual(len(res), 10)
        self.assertIsNotNone(res.get('ordering'))
        self.assertIsNotNone(res.get('option_ordering'))
        self.assertTrue(isinstance(res.get('report_date'), datetime.date))

    def test_get_contacts(self):
        """ get xls list array of contacts data """
        with self.assertLessNumQueries(46):
            res = _get_contacts(self.company)

        self.assertTrue(len(res) > 1)
        self.assertEqual(len(res[0]), 14)
        self.assertEqual(len(res[1]), 14)  # no nationality
        self.assertIn(u'999ü', [r[0] for r in res])

    def test_get_default_context(self):
        """ default context for pdf exports """
        res = _get_default_pdf_context(self.company, timezone.now().date())
        self.assertEqual(res.keys(), ['currency', 'company', 'report_date',
                                      'today', 'pagesize'])

    def test_get_vested_shares_pdf_context(self):
        """ get context for pdf with vested shares export """
        pos = self.company.shareholder_set.first().buyer.first()
        pos.vesting_months = 99
        pos.save()
        res = _get_vested_shares_pdf_context(
            self.company, timezone.now().date())
        self.assertEqual(res.keys(), ['pagesize', 'table_data', 'company',
                                      'currency', 'header', 'report_date',
                                      'heading', 'today'])
        self.assertEqual(len(res['table_data']), 1)

    def test_parse_ordering(self):
        """ convert ordering param from FE to ORM ready ordering """

        self.assertEqual(_parse_ordering(None), 'user__last_name')
        self.assertEqual(_parse_ordering('test_desc'), '-test')
        self.assertEqual(_parse_ordering('test'), 'test')

    def test_order_queryset(self):
        """ order queryset by field or method """
        qs = Shareholder.objects.all()
        self.assertEqual(list(_order_queryset(qs, 'pk')),
                         list(qs.order_by('pk')))

        self.assertEqual(list(_order_queryset(qs, '-pk')),
                         list(qs.order_by('-pk')))

    def test_order_queryset_share_count(self):
        """ order queryset by field or method """
        qs = Shareholder.objects.all()
        # desc share count
        res = _order_queryset(qs, '-share_count')
        for idx, r in enumerate(res):
            if idx > 0:
                self.assertTrue(r.share_count() <= res[idx-1].share_count())

        # asc share_count
        res = _order_queryset(qs, 'share_count')
        for idx, r in enumerate(res):
            if idx > 0:
                self.assertTrue(r.share_count() >= res[idx-1].share_count())

    def test_order_queryset_user__email(self):
        company = CompanyGenerator().generate()
        mommy.make(Shareholder, company=company, _quantity=10,
                   _fill_optional=True)
        qs = company.shareholder_set.all()
        for idx, s in enumerate(qs):
            s.user.email = u'{}@example.com'.format(idx)
            s.user.save()

        res = _order_queryset(qs, 'user__email')
        for idx, r in enumerate(res):
            if idx > 0:
                self.assertNotEqual(r.user.email, '')
                self.assertIn(u'@', r.user.email)
                self.assertGreater(r.user.email, res[idx-1].user.email)

        res = _order_queryset(qs, '-user__email')
        for idx, r in enumerate(res):
            if idx > 0:
                self.assertLess(r.user.email, res[idx-1].user.email)

    def test_order_queryset_cumulated_face_value(self):
        qs = Shareholder.objects.all()
        cs = qs.last()
        for idx, s in enumerate(qs):
            mommy.make('shareholder.Position', seller=cs, buyer=s, count=idx)

        res = _order_queryset(qs, 'cumulated_face_value')
        for idx, r in enumerate(res):
            if idx > 0:
                self.assertGreaterEqual(r.cumulated_face_value(),
                                        res[idx-1].cumulated_face_value())

        res = _order_queryset(qs, '-cumulated_face_value')
        for idx, r in enumerate(res):
            if idx > 0:
                self.assertLessEqual(r.cumulated_face_value(),
                                     res[idx-1].cumulated_face_value())

    def test_order_queryset_postal_code(self):
        qs = Shareholder.objects.all()
        for idx, s in enumerate(qs):
            s.user.userprofile.postal_code = u'{}'.format(idx)
            s.user.userprofile.save()

        res = _order_queryset(qs, 'user__userprofile__postal_code')
        for idx, r in enumerate(res):
            if idx > 0:
                self.assertGreater(r.user.userprofile.postal_code,
                                   res[idx-1].user.userprofile.postal_code)

        res = _order_queryset(qs, '-user__userprofile__postal_code')
        for idx, r in enumerate(res):
            if idx > 0:
                self.assertLess(r.user.userprofile.postal_code,
                                res[idx-1].user.userprofile.postal_code)

    def test_order_queryset_company_name(self):
        """ sort for last_name also should sort company names """
        qs = Shareholder.objects.all()
        for idx, s in enumerate(qs):
            s.user.userprofile.company_name = str(unichr(idx+97))
            s.user.first_name = u''
            s.user.last_name = u''
            s.user.save()
            s.user.userprofile.save()

        res = _order_queryset(qs, 'get_full_name')
        for idx, r in enumerate(res):
            if idx > 0:
                self.assertGreater(r.get_full_name(),
                                   res[idx-1].get_full_name())

        res = _order_queryset(qs, '-get_full_name')
        for idx, r in enumerate(res):
            if idx > 0:
                self.assertLess(r.get_full_name(),
                                res[idx-1].get_full_name())

    def test_add_file_to_report(self):
        """ attach file to report model """
        report = ReportGenerator().generate()
        _add_file_to_report(
          u'somefilename.xls', report, 'some file content')
        report.refresh_from_db()
        with open(report.file.path) as f:
            self.assertEqual(f.read(), 'some file content')

    def test_summarize_report(self):
        """ record some data when report finished rendering """
        started_at = timezone.now()
        report = ReportGenerator().generate()
        _summarize_report(report, started_at)
        report.refresh_from_db()
        self.assertIsNotNone(report.generation_time)
        self.assertIsNotNone(report.generated_at)

    def test_send_notify(self):
        """ send message about finished report """
        report = ReportGenerator().generate()
        report.render()
        _send_notify(report.user, 'somefilename.pdf', 'test subject',
                     'test body', 'file desc', report.get_absolute_url())

        self.assertEqual(mail.outbox[0].subject, 'test subject')
        self.assertEqual(mail.outbox[0].to, [report.user.email])

    def test_get_filename(self):
        """ render filename for report """
        report = ReportGenerator().generate()
        filename = _get_filename(report, report.company)
        self.assertEqual(filename.count('_'), 3)
        self.assertIn(slugify(report.company.name), filename)
        self.assertTrue(filename.endswith('pdf'))

    def test_prepare_report(self):
        """ create report obj and set eta """
        company = CompanyGenerator().generate()
        report = _prepare_report(company, 'captable', 'share_count', 'PDF')
        self.assertIsNotNone(report.eta)
        self.assertIsNotNone(report.file_type)
        self.assertIsNotNone(report.report_type)

    def test_render_address_data_xls(self):
        report = ReportGenerator().generate(company=self.company,
                                            report_type='address_data',
                                            file_type='XLS')
        PositionGenerator().generate(company=report.company, seller=None)
        render_address_data_xls(
            report.company.pk, report.pk,
            user_id=report.user.pk, ordering=None,
            notify=True, track_downloads=False)
        report.refresh_from_db()

        self.assertIsNotNone(report.file)

    def test_render_address_data_pdf(self):
        report = ReportGenerator().generate(company=self.company,
                                            report_type='address_data',
                                            file_type='PDF')
        PositionGenerator().generate(company=report.company, seller=None)
        render_address_data_pdf(
            report.company.pk, report.pk,
            user_id=report.user.pk, ordering=None,
            notify=True, track_downloads=False)
        report.refresh_from_db()

        self.assertIsNotNone(report.file)

    def test_render_address_data_pdf_performance(self):
        """ ensure we don't run into https://goo.gl/qKRyQx """
        start = timezone.now()
        report = ReportGenerator().generate(company=self.company,
                                            report_type='address_data',
                                            file_type='PDF')
        # seed more capital
        mommy.make('shareholder.Position',
                   buyer=self.company.get_company_shareholder(),
                   seller=None, count=1000000, security=self.sec)
        # mass shareholder creation
        for x in range(0, 600):
            shareholder = mommy.make('shareholder.Shareholder',
                                     company=self.company)
            mommy.make('shareholder.Position',
                       seller=self.company.get_company_shareholder(),
                       buyer=shareholder, count=1, security=self.sec)
        # logger.warning('finished test data creation: {}'.format(
        #     timezone.now()-start))

        render_address_data_pdf(
            report.company.pk, report.pk,
            user_id=report.user.pk, ordering=None,
            notify=True, track_downloads=False)
        report.refresh_from_db()
        # logger.warning('finished pdf rendering: {}'.format(
        #     timezone.now()-start))

        self.assertIsNotNone(report.file)
        delta = timezone.now()-start
        self.assertLess(delta.seconds, 120)

    def test_render_assembly_participation_xls(self):
        """ render csv with assembly participants """
        report = ReportGenerator().generate(company=self.company)
        PositionGenerator().generate(company=report.company, seller=None)
        render_assembly_participation_xls(
            report.company.pk, report.pk,
            user_id=report.user.pk, ordering=None,
            notify=True, track_downloads=False)
        report.refresh_from_db()

        self.assertIsNotNone(report.file)

    def test_render_assembly_participation_pdf(self):
        report = ReportGenerator().generate(company=self.company)
        PositionGenerator().generate(company=report.company, seller=None)
        render_assembly_participation_pdf(
            report.company.pk, report.pk,
            user_id=report.user.pk, ordering=None,
            notify=True, track_downloads=False)
        report.refresh_from_db()

        self.assertIsNotNone(report.file)

    def test_render_captable_pdf(self):
        report = ReportGenerator().generate(company=self.company)
        # FIXME way tooooo many queries for 13 shs, just calculate how this
        # would be for 10.000 shs
        with self.assertLessNumQueries(533):
            render_captable_pdf(report.company.pk, report.pk,
                                user_id=report.user.pk, ordering=None,
                                notify=True, track_downloads=False)
        report.refresh_from_db()

        self.assertIsNotNone(report.file)

    def test_render_captable_xls(self):
        report = ReportGenerator().generate(file_type='XLS',
                                            company=self.company)
        PositionGenerator().generate(company=report.company, seller=None)
        render_captable_xls(report.company.pk, report.pk,
                            user_id=report.user.pk, ordering=None,
                            notify=True, track_downloads=False)
        report.refresh_from_db()

        self.assertIsNotNone(report.file)

    def test_render_certificates_xls(self):
        report = ReportGenerator().generate(company=self.company,
                                            report_type='certificates',
                                            file_type='XLS')
        PositionGenerator().generate(company=report.company, seller=None)
        render_certificates_xls(
            report.company.pk, report.pk,
            user_id=report.user.pk, ordering=None,
            notify=True, track_downloads=False)
        report.refresh_from_db()

        self.assertIsNotNone(report.file)

    def test_render_certificates_pdf(self):
        report = ReportGenerator().generate(company=self.company,
                                            report_type='certificates',
                                            file_type='PDF')
        PositionGenerator().generate(company=report.company, seller=None)
        render_certificates_pdf(
            report.company.pk, report.pk,
            user_id=report.user.pk, ordering=None,
            notify=True, track_downloads=False)
        report.refresh_from_db()

        self.assertIsNotNone(report.file)

    def test_render_vested_shares_xls(self):
        report = ReportGenerator().generate(company=self.company,
                                            report_type='vested_shares',
                                            file_type='XLS')
        PositionGenerator().generate(company=report.company, seller=None)
        render_vested_shares_xls(
            report.company.pk, report.pk,
            user_id=report.user.pk, ordering=None,
            notify=True, track_downloads=False)
        report.refresh_from_db()

        self.assertIsNotNone(report.file)

    def test_render_vested_shares_pdf(self):
        report = ReportGenerator().generate(company=self.company,
                                            report_type='vested_shares',
                                            file_type='PDF')
        PositionGenerator().generate(company=report.company, seller=None)
        render_vested_shares_pdf(
            report.company.pk, report.pk,
            user_id=report.user.pk, ordering=None,
            notify=True, track_downloads=False)
        report.refresh_from_db()

        self.assertIsNotNone(report.file)

    @patch('reports.tasks.render_assembly_participation_xls.apply_async')
    @patch('reports.tasks.render_captable_pdf.apply_async')
    @patch('reports.tasks.render_captable_xls.apply_async')
    def test_prerender_reports(self, mock_xls, mock_pdf,
                               mock_assembly_participation_xls):
        """ render every night the reports for all corps """
        # corps not needing a report = noise
        CompanyGenerator().generate()
        ReportGenerator().generate()

        prerender_reports()

        company = self.shs[0].company
        pdf_report = company.report_set.filter(file_type='PDF',
                                               report_type='captable').last()
        xls_ass_report = company.report_set.filter(
            file_type='XLS', report_type='assembly_participation').last()
        xls_report = company.report_set.filter(file_type='XLS',
                                               report_type='captable').last()
        self.assertEqual(mock_pdf.call_count, 14)
        mock_pdf.assert_called_with(
            args=[company.pk, pdf_report.pk],
            kwargs={'ordering': pdf_report.order_by})
        self.assertEqual(mock_xls.call_count, 14)
        mock_xls.assert_called_with(
            args=[company.pk, xls_report.pk],
            kwargs={'ordering': xls_report.order_by})
        self.assertEqual(mock_assembly_participation_xls.call_count, 1)
        mock_assembly_participation_xls.assert_called_with(
            args=[company.pk, xls_ass_report.pk],
            kwargs={'ordering': xls_ass_report.order_by})
