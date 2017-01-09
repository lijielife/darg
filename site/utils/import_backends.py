#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import datetime
import logging

from django.contrib.auth.models import User
from django.db import DataError
from django.utils.text import slugify
from django.utils.translation import gettext as _

from project.generators import DEFAULT_TEST_DATA, OperatorGenerator, _make_user
from shareholder.models import (REGISTRATION_TYPES, Company, OptionPlan,
                                OptionTransaction, Position, Security,
                                Shareholder, UserProfile)

SISWARE_CSV_HEADER = [
    u'Aktion\xe4rID', u'Aktion\xe4rsArt', u'Eintragungsart', u'Suchname',
    u'Firmaname', u'FirmaAbteilung', u'Titel', u'Anrede', u'Vorname',
    u'Vorname Zusatz', u'Name', u'Adresse', u'Adresse2', u'Postfach',
    u'Nr Postfach', u'PLZ', u'Ort', u'Land', u'C/O', u'Geburtsdatum',
    u'Sprache', u'VersandArt', u'Nationalit\xe4t', u'AktienArt', u'Valoren-Nr',
    u'Nennwert', u'Anzahl Aktien', u'Zertifikat-Nr', u'Ausgestellt am',
    u'Skontro-Nr', u'DepotArt'
]

logger = logging.getLogger(__name__)


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
            self.company_shareholder = Shareholder.objects.create(
                company=self.company, number=0, user=_make_user())

        # and a matching operator?
        self.operator = self.company.operator_set.first()
        if not self.operator:
            logger.info('operator created')
            self.operator = OperatorGenerator().generate(
                company=self.company)
            print u'operator created with username {} and pw {}'.format(
                self.operator.user.username, DEFAULT_TEST_DATA.get('password'))

    def _import_row(self, row):
        """
        import a single line of the data set
        """
        if not [field for field in row if field != u'']:
            return 0

        # USER
        user = self._get_or_create_user(
            row[0], row[8]+' '+row[9], row[10], row[1],
            company=row[4], department=row[5])
        # SHAREHOLDER
        shareholder = self._get_or_create_shareholder(row[0], user)
        # POSITION
        if not row[27]:
            self._get_or_create_position(
                bought_at=row[28], buyer=shareholder, count=row[26],
                value=row[25],
                face_value=float(row[25].replace(',', '.')),
                registration_type=row[2]
            )
        # OPTION + PLAN
        else:
            self._get_or_create_option_transaction(
                cert_id=row[27], bought_at=row[28], buyer=shareholder,
                count=row[26], face_value=float(row[25].replace(',', '.')),
                registration_type=row[2]
            )

        return 1

    def _finish_import(self):
        """
        check data consistency, company data, total sums to ensure the import is
        fully valid
        """
        # FIXME update security.count
        logger.warning('import finishing not implemented')

    def _get_or_create_shareholder(self, shareholder_number, user):
        shareholder, c_ = Shareholder.objects.get_or_create(
            number=shareholder_number, company=self.company,
            defaults={'company': self.company,
                      'number': shareholder_number,
                      'user': user
                      }
        )
        return shareholder

    def _get_or_create_security(self, face_value):

        security, c_ = Security.objects.get_or_create(
            title='R', face_value=face_value,
            company=self.company, count=1)  # count=1 intermediary

        return security

    def _get_or_create_position(self, bought_at, buyer, count, value,
                                face_value, registration_type, **kwargs):
        """
        we have no history data, hence, we start with an initial position/
        transaction of the day of the import
        """
        seller = self.company.get_company_shareholder()
        security = self._get_or_create_security(face_value)
        registration_type = self._match_registration_type(registration_type)

        # FIXME add scontro and depot type to lookup
        position, c_ = Position.objects.get_or_create(
            bought_at=bought_at[0:10], seller=seller, buyer=buyer,
            security=security, count=int(count),
            defaults={
                'value': float(value.replace(',', '.')),
                'registration_type': registration_type,
            })

        if not c_:
            print (u'position for {} "{} {}"->"{} {}" {} with pk {} existing'
                   u''.format(
                    bought_at, seller.user.first_name, seller.user.last_name,
                    buyer.user.first_name, buyer.user.last_name, security,
                    position.pk))

        return position

    def _get_or_create_option_transaction(self, cert_id, bought_at, buyer,
                                          count, face_value, registration_type):

        registration_type = self._match_registration_type(registration_type)

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
                'registration_type': registration_type
            })

        return option

    def _get_or_create_user(self, shareholder_id, first_name, last_name,
                            legal_entity, company, department):
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

        l = 'H' if 'Jurist' not in legal_entity else 'C'
        if hasattr(user, 'userprofile'):
            profile = user.userprofile
            profile.legal_type = l
            profile.company_name = company
            if department:
                profile.company_department = department
            profile.save()
        elif not hasattr(user, 'userprofile'):
            UserProfile.objects.create(user=user, legal_type=l,
                                       company_name=company)

        return user

    def _match_registration_type(self, registration_type):
        if registration_type == u'Eigene Rechnung':
            return REGISTRATION_TYPES[1][0]
        if registration_type == u'Eigenbestand':
            return REGISTRATION_TYPES[0][0]

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

