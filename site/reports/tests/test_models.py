#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
from mock import patch

from django.test import TestCase
from django.utils import timezone

from project.generators import ReportGenerator
from reports.models import get_report_upload_path


class ReportModelTestCase(TestCase):

    def setUp(self):
        self.report = ReportGenerator().generate(
            file_type='PDF', report_type='captable')

    def test_get_report_upload_path(self):
        """ render path for saving prive files for reports """
        path = get_report_upload_path(self.report, 'some-report-filename.pdf')
        self.assertEqual(path, 'private/reports/{}/{}/some-report-filename.pdf'
                         ''.format(self.report.company.pk, self.report.pk))

    def test_get_absolute_url(self):
        """ get path to download report file """
        url = self.report.get_absolute_url()
        self.assertEqual(url, '/reports/{}/download'.format(self.report.pk))

    @patch('reports.tasks.render_vested_shares_pdf.apply_async')
    @patch('reports.tasks.render_captable_pdf.apply_async')
    @patch('reports.tasks.render_assembly_participation_xls.apply_async')
    @patch('reports.tasks.render_assembly_participation_pdf.apply_async')
    def test_render(self, mock_participation_pdf_task, mock_participation_task,
                    mock_task, mock_vested_task):
        """ trigger rendering of report file """
        # FIXME iterate over constant from models
        self.report.render()
        self.assertTrue(mock_task.called)

        self.report.report_type = 'assembly_participation'
        self.report.file_type = 'XLS'
        self.report.save()
        self.report.render()
        self.assertTrue(mock_participation_task.called)

        self.report.report_type = 'assembly_participation'
        self.report.file_type = 'PDF'
        self.report.save()
        self.report.render()
        self.assertTrue(mock_participation_pdf_task.called)

        self.report.report_type = 'vested_shares'
        self.report.file_type = 'PDF'
        self.report.save()
        self.report.render()
        self.assertTrue(mock_vested_task.called)

    def test_update_eta(self):
        """ calculate and update eta """
        self.report.update_eta()
        self.report.refresh_from_db()
        self.assertTrue(
            self.report.eta > timezone.now() + datetime.timedelta(seconds=170))

    def test_update_eta_from_prev_report(self):
        """ calculate and update eta with prev reports existing"""
        report = ReportGenerator().generate(
            company=self.report.company, file_type='PDF',
            report_type='captable')
        report.generation_time = 60
        report.save()

        self.report.update_eta()
        self.report.refresh_from_db()
        self.assertTrue(
            self.report.eta < timezone.now() + datetime.timedelta(seconds=70))
        self.assertTrue(
            self.report.eta > timezone.now() + datetime.timedelta(seconds=50))
