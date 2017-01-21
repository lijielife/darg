#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import datetime
import logging

from dateutil.parser import parse
from django.contrib.auth.models import User
from django.db import DataError
from django.utils.text import slugify
from django.utils.translation import gettext as _

from project.generators import DEFAULT_TEST_DATA, OperatorGenerator, _make_user
from shareholder.models import (DEPOT_TYPES, REGISTRATION_TYPES, Company,
                                Country, OptionPlan, OptionTransaction,
                                Position, Security, Shareholder, UserProfile)
from utils.geo import COUNTRY_MAP, _get_language_iso_code

SISWARE_CSV_HEADER = [
    # 0
    u'Aktion\xe4rID', u'Aktion\xe4rsArt', u'Eintragungsart', u'Suchname',
    # 4
    u'Firmaname', u'FirmaAbteilung', u'Titel', u'Anrede', u'Vorname',
    # 9
    u'Vorname Zusatz', u'Name', u'Adresse', u'Adresse2', u'Postfach',
    # 14
    u'Nr Postfach', u'PLZ', u'Ort', u'Land', u'C/O', u'Geburtsdatum',
    # 20
    u'Sprache', u'VersandArt', u'Nationalit\xe4t', u'AktienArt', u'Valoren-Nr',
    # 25
    u'Nennwert', u'Anzahl Aktien', u'Zertifikat-Nr', u'Ausgestellt am',
    # 29
    u'Skontro-Nr', u'DepotArt'
]

logger = logging.getLogger(__name__)

COMPANY_SHAREHOLDER_NUMBER = 1913  # RFB AG


class BaseImportBackend(object):
    """
    common logic to import captable data from a source into a companies account
    """

    def __init__(self, filename):

        self.filename = filename
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

    def to_unicode(self, value):
        if isinstance(value, list):
            return [unicode(el, 'utf8') for el in value]
        else:
            return unicode(value, 'utf8')


class SisWareImportBackend(BaseImportBackend):
    """
    import from sisware share register in switzerland

    import does not import history, it creates an initial transaction and
    assumes that the share register starts with the import
    """

    file_content = []

    def _init_import(self, company_pk):
        """
        check and/or prepare data required for the import

        security not treated here, will be created upon existence while parsing
        the rows
        """
        # do we have a company?
        try:
            self.company = Company.objects.get(pk=company_pk)
        except Company.DoesNotExist:
            raise ValueError('company not existing. please create company and '
                             'operator first')

        # with a company shareholder?
        try:
            self.company_shareholder = self.company.get_company_shareholder()
        except ValueError:
            # import based in setting
            row = self._find_row(column=0, needle=COMPANY_SHAREHOLDER_NUMBER)
            user = self._get_or_create_user(
                shareholder_id=row[0], first_name=row[8]+' '+row[9],
                last_name=row[10], legal_type=row[1], company=row[4],
                department=row[5], title=row[6], salutation=row[7], street=row[12],
                street2=row[12], pobox=row[14], postal_code=row[15],
                city=row[16], country=row[17], language=row[20], birthday=row[19],
                c_o=row[18], nationality=row[22])
            self._get_or_create_shareholder(row[0], user,
                                                          mailing_type=row[21])

        # and a matching operator?
        self.operator = self.company.operator_set.first()
        if not self.operator:
            logger.info('operator created')
            self.operator = OperatorGenerator().generate(
                company=self.company)
            print u'operator created with username {} and pw {}'.format(
                self.operator.user.username, DEFAULT_TEST_DATA.get('password'))

        # check if we can import all countries
        countries = []
        with open(self.filename) as f:
            reader = csv.reader(f, delimiter=';', dialect=csv.excel)
            self.row_count = 0
            for row in reader:
                row = [self.to_unicode(field) for field in row]
                if row == SISWARE_CSV_HEADER:
                    continue
                if row[17]:
                    countries.append(row[17])
        countries = set(countries)
        missing_countries = []
        for country in countries:
            if country not in COUNTRY_MAP.keys():
                missing_countries.append(country)
        if missing_countries:
            raise ValueError('cannot map countries to db objs: {}. '
                             'import not started'.format(missing_countries))

        # check if we can import all nationalities
        countries = []
        with open(self.filename) as f:
            reader = csv.reader(f, delimiter=';', dialect=csv.excel)
            self.row_count = 0
            for row in reader:
                row = [self.to_unicode(field) for field in row]
                if row == SISWARE_CSV_HEADER:
                    continue
                if row[22]:
                    countries.append(row[22])
        countries = set(countries)
        missing_countries = []
        for country in countries:
            if country not in COUNTRY_MAP.keys():
                missing_countries.append(country)
        if missing_countries:
            raise ValueError('cannot map nationalities to db objs: {}. '
                             'import not started'.format(missing_countries))

        # check if we can map all languages
        languages = []
        with open(self.filename) as f:
            reader = csv.reader(f, delimiter=';', dialect=csv.excel)
            self.row_count = 0
            for row in reader:
                row = [self.to_unicode(field) for field in row]
                if row == SISWARE_CSV_HEADER:
                    continue
                if row[20]:
                    languages.append(row[20])
        languages = set(languages)
        missing = []
        for language in languages:
            if not _get_language_iso_code(language):
                missing.append(language)
        if missing:
            raise ValueError('cannot map languages to db objs: {}. '
                             'import not started.'.format(missing))

    def _import_row(self, row):
        """
        import a single line of the data set
        """
        if not [field for field in row if field != u'']:
            return 0

        # USER
        user = self._get_or_create_user(
            shareholder_id=row[0], first_name=row[8]+' '+row[9],
            last_name=row[10], legal_type=row[1], company=row[4],
            department=row[5], title=row[6], salutation=row[7], street=row[12],
            street2=row[12], pobox=row[14], postal_code=row[15],
            city=row[16], country=row[17], language=row[20], birthday=row[19],
            c_o=row[18], nationality=row[22])
        # SHAREHOLDER
        shareholder = self._get_or_create_shareholder(row[0], user,
                                                      mailing_type=row[21])
        # SECURITY
        self._get_or_create_security(
            face_value=float(row[25].replace(',', '.')), cusip=row[24])

        # POSITION
        if not row[27]:
            self._get_or_create_position(
                bought_at=row[28], buyer=shareholder, count=row[26],
                value=row[25],
                face_value=float(row[25].replace(',', '.')),
                registration_type=row[2],
                stock_book_id=row[29], depot_type=row[30]
            )
        # OPTION + PLAN
        else:
            self._get_or_create_option_transaction(
                cert_id=row[27], bought_at=row[28], buyer=shareholder,
                count=row[26], face_value=float(row[25].replace(',', '.')),
                registration_type=row[2], certificate_id=row[27],
                stock_book_id=row[29], depot_type=row[30]
            )

        return 1

    def _find_row(self, column, needle):
        with open(self.filename) as f:
            reader = csv.reader(f, delimiter=';', dialect=csv.excel)
            for row in reader:
                row = [self.to_unicode(field) for field in row]
                if row == SISWARE_CSV_HEADER:
                    continue
                if row[column] == str(needle):
                    return row

    def _finish_import(self):
        """
        check data consistency, company data, total sums to ensure the import is
        fully valid
        """
        # FIXME update security.count
        logger.warning('import finishing not implemented')

    def _get_or_create_shareholder(self, shareholder_number, user,
                                   mailing_type):
        MAILING_TYPE_MAP = {
            'Papier': '1',
            'Unzustellbar': '0',
        }
        mailing_type = MAILING_TYPE_MAP[mailing_type]
        shareholder, c_ = Shareholder.objects.get_or_create(
            number=shareholder_number, company=self.company,
            defaults={'company': self.company,
                      'number': shareholder_number,
                      'user': user,
                      'mailing_type': mailing_type
                      }
        )
        return shareholder

    def _get_or_create_security(self, face_value, cusip=None):

        kwargs = {'count': 1}
        if cusip:
            kwargs.update({'cusip': cusip})

        security, c_ = Security.objects.get_or_create(
            title='R', face_value=face_value,
            company=self.company, defaults=kwargs)  # count=1 intermediary

        return security

    def _get_or_create_position(self, bought_at, buyer, count, value,
                                face_value, registration_type, stock_book_id,
                                depot_type, **kwargs):
        """
        we have no history data, hence, we start with an initial position/
        transaction of the day of the import
        """
        seller = self.company.get_company_shareholder()
        security = self._get_or_create_security(face_value)
        registration_type = self._match_registration_type(registration_type)
        depot_type = self._match_depot_type(depot_type)

        # FIXME add scontro and depot type to lookup
        position, c_ = Position.objects.get_or_create(
            bought_at=bought_at[0:10], seller=seller, buyer=buyer,
            security=security, count=int(count),
            defaults={
                'value': float(value.replace(',', '.')),
                'registration_type': registration_type,
                'stock_book_id': stock_book_id,
                'depot_type': depot_type,
            })

        if not c_:
            print (u'position for {} "{} {}"->"{} {}" {} with pk {} existing'
                   u''.format(
                    bought_at, seller.user.first_name, seller.user.last_name,
                    buyer.user.first_name, buyer.user.last_name, security,
                    position.pk))

        return position

    def _get_or_create_option_transaction(self, cert_id, bought_at, buyer,
                                          count, face_value, registration_type,
                                          certificate_id, stock_book_id,
                                          depot_type):

        registration_type = self._match_registration_type(registration_type)
        depot_type = self._match_depot_type(depot_type)

        security = self._get_or_create_security(face_value)
        option_plan, c_ = OptionPlan.objects.get_or_create(
            company=self.company, security=security,
            defaults={
                'title': _('Default OptionPlan for {}').format(security),
                'count': 0,
                'exercise_price': 1,
                'board_approved_at': datetime.datetime(2013, 1, 1),
            })
        seller = self.company.get_company_shareholder()

        option, c_ = OptionTransaction.objects.get_or_create(
            certificate_id=cert_id, bought_at=bought_at[0:10], buyer=buyer,
            seller=seller, count=count, option_plan=option_plan,
            defaults={
                'registration_type': registration_type,
                'certificate_id': certificate_id,
                'depot_type': depot_type,
                'stock_book_id': stock_book_id,
            })

        return option

    def _get_or_create_user(self, shareholder_id, first_name, last_name,
                            legal_type, company, department, title,
                            salutation, street, street2, pobox,
                            postal_code, city, country, language, birthday,
                            c_o, nationality,):
        """
        we have no email to identify duplicates and merge then. hence we are
        using the shareholder id to create new users for each shareholder id
        """
        username = u"{}-{}".format(slugify(self.company.name), shareholder_id)
        try:
            user, c_ = User.objects.get_or_create(
                username=username[:29],
                defaults={u'first_name': first_name, u'last_name': last_name}
            )
        except DataError as e:
            # some users might have last name exceeding max length.
            print (u'create user failed for {} {}. please fix data & reimport.'
                   u'hint: check string length'.format(first_name, last_name))
            raise e

        kwargs = dict(
            legal_type='H' if 'Jurist' not in legal_type else 'C',
            company_name=company,
            company_department=department,
            title=title,
            salutation=salutation,
            street=street,
            street2=street2,
            pobox=pobox,
            postal_code=postal_code,
            city=city,
            c_o=c_o,
        )
        # FIXME use proper country name translation
        if country and COUNTRY_MAP[country]:
            kwargs.update(
                {'country': Country.objects.get(iso_code=COUNTRY_MAP[country])})
        if birthday:
            kwargs.update({'birthday': parse(birthday)})
        if nationality and COUNTRY_MAP[nationality]:
            kwargs.update(
                {'nationality': Country.objects.get(
                    iso_code=COUNTRY_MAP[nationality])})
        if language:
            kwargs.update({'language': _get_language_iso_code(language)})

        # save
        if hasattr(user, 'userprofile'):
            profile = user.userprofile
            for (key, value) in kwargs.items():
                setattr(profile, key, value)
            profile.save()
        elif not hasattr(user, 'userprofile'):
            UserProfile.objects.create(user=user, **kwargs)

        return user

    def _match_registration_type(self, registration_type):
        if registration_type == u'Eigene Rechnung':
            return REGISTRATION_TYPES[1][0]
        if registration_type == u'Eigenbestand':
            return REGISTRATION_TYPES[0][0]

    def _match_depot_type(self, depot_type):
        if depot_type == u'Zertifikatsdepot':
            return DEPOT_TYPES[0][0]
        if depot_type == u'Gesellschaftsdepot':
            return DEPOT_TYPES[1][0]
        if depot_type == u'Sperrdepot':
            return DEPOT_TYPES[2][0]


    def validate(self, filename):
        """
        validate if file can be used
        """
        with open(filename) as f:
            reader = csv.reader(f, delimiter=';', dialect=csv.excel)
            for row in reader:
                row = [self.to_unicode(field) for field in row]
                if row == SISWARE_CSV_HEADER:
                    break
                else:
                    raise ValueError('invalid file for sisware import backend')

    def import_from_file(self, company_pk):
        """
        read file contents and place them into the database
        """

        self._init_import(company_pk)

        with open(self.filename) as f:
            reader = csv.reader(f, delimiter=';', dialect=csv.excel)
            self.row_count = 0
            for row in reader:
                row = [self.to_unicode(field) for field in row]
                if row == SISWARE_CSV_HEADER:
                    continue
                self.file_content.append(','.join(row))
                self.row_count += self._import_row(row)

        self._finish_import()

        return self.row_count

# reusable  list of available import backends
IMPORT_BACKENDS = [
    SisWareImportBackend,
]

