#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv

from shareholder.models import Company

SISWARE_CSV_HEADER = [
    'Aktion\x8arID', 'Aktion\x8arsArt', 'Eintragungsart', 'Suchname',
    'Firmaname', 'FirmaAbteilung', 'Titel', 'Anrede', 'Vorname',
    'Vorname Zusatz', 'Name', 'Adresse', 'Adresse2', 'Postfach', 'Nr Postfach',
    'PLZ', 'Ort', 'Land', 'C/O', 'Geburtsdatum', 'Sprache', 'VersandArt',
    'Nationalit\x8at', 'AktienArt', 'Valoren-Nr', 'Nennwert', 'Anzahl Aktien',
    'Zertifikat-Nr', 'Ausgestellt am', 'Skontro-Nr', 'DepotArt'
]


class BaseImportBackend(object):
    """
    common logic to import captable data from a source into a companies account
    """

    def __init__(self, filename):

        self.validate(filename)

    def validate(self, filename):
        """
        is this a good file for this backend?
        """
        raise NotImplementedError('create me!')

    def import_from_file(self, filename, company_pk):
        """
        read file contents and place them into the database
        """
        raise NotImplementedError('create me!')


class SisWareImportBackend(BaseImportBackend):
    """
    import from sisware share register in switzerland
    """

    def _init_import(self, company_pk):
        """
        check and/or prepare data required for the import
        """
        try:
            Company.objects.get(pk=company_pk)
        except Company.DoesNotExist:
            raise ValueError('company not existing. please create company and '
                             'operator first')

    def _import_row(self, row):
        """
        import a single line of the data set
        """
        if not [field for field in row if field != u'']:
            return 0

        self._get_or_create_shareholder()
        self._get_or_create_position()

        return 1

    def _finish_import(self):
        """
        check data consistency, company data, total sums to ensure the import is
        fully valid
        """
        raise NotImplementedError('import finishing not implemented')

    def _get_or_create_shareholder(self, **kwargs):
        pass

    def _get_or_create_position(self, **kwargs):
        pass

    def validate(self, filename):
        with open(filename) as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                if row == SISWARE_CSV_HEADER:
                    break
                else:
                    raise ValueError('invalid file for sisware import backend')

    def import_from_file(self, filename, company_pk):
        """
        read file contents and place them into the database
        """
        self._init_import(company_pk)
        with open(filename) as f:
            reader = csv.reader(f, delimiter=';')
            count = 0
            for row in reader:
                if row == SISWARE_CSV_HEADER:
                    continue
                count += self._import_row(row)

        self._finish_import()

        return count

# reusable  list of available import backends
IMPORT_BACKENDS = [
    SisWareImportBackend,
]
