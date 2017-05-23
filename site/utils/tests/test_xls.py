import os

from django.test import TestCase
from django.utils.translation import ugettext as _
from model_mommy import mommy

from shareholder.models import Shareholder
from utils.xls import save_to_excel_file


class ExcelTestCase(TestCase):
    """ write to xlsx files """

    def test_save_to_excel_file(self):

        filename = 'example.xlsx'
        mommy.make('shareholder.Shareholder', _quantity=10)
        header = [(_('ID'), _('shareholder number'), _('Company Name'))]
        data = Shareholder.objects.all().values_list(
            'pk', 'number', 'company__name')
        save_to_excel_file(filename, list(data), header)
        os.remove(filename)
