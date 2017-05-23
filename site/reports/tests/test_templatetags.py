
from dateutil.relativedelta import relativedelta
from django.test import TestCase
from django.utils import timezone

from project.generators import ComplexShareholderConstellationGenerator
from reports.templatetags.report_tags import (get_active_option_holders,
                                              get_active_shareholders)


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
            self.security, self.today, self.ordering)
        self.assertQuerysetEqual(res, self.company.shareholder_set.none())
