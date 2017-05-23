
from dateutil.relativedelta import relativedelta
from django.test import TestCase
from django.utils import timezone

from project.generators import ComplexShareholderConstellationGenerator
from reports.templatetags.report_tags import (get_active_option_holders,
                                              get_active_shareholders,
                                              shareholder_cumulated_face_value)


class ReportTemplateTagTestCase(TestCase):

    def setUp(self):
        self.shs, self.security = (
            ComplexShareholderConstellationGenerator().generate())
        self.company = self.shs[0].company
        self.ordering = '-share_count'
        self.today = timezone.now().date()
        self.oneyearago = self.today - relativedelta(years=1)

    def test_get_active_shareholders(self):
        """ return ordered list of active sharehholders for security on date """
        res = get_active_shareholders(self.company, self.today, self.ordering)
        self.assertEqual(len(res), 11)

    def test_get_active_option_holders(self):
        """ return ordered list of active option holders for security on date
        """
        res = get_active_option_holders(
            self.company, self.today, self.ordering)
        self.assertQuerysetEqual(res, self.company.shareholder_set.none())

    def test_shareholder_cumulated_face_value(self):
        """ return cumulated face value for single shareholder """
        res = shareholder_cumulated_face_value(self.shs[1], self.today)
        self.assertEqual(self.shs[1].cumulated_face_value(date=self.today),
                         res)
