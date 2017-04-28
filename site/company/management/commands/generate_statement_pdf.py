#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
from django.utils import timezone
from shareholder.models import Company
"""

from django.core.management import BaseCommand
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

from shareholder.models import Shareholder, Company


class Command(BaseCommand):

    help = _('Generate Report for one or all shareholders')

    def add_arguments(self, parser):  # pragma: no cover
        parser.add_argument('company_pk', nargs='+', type=int)

        parser.add_argument(
            '--shareholder_pk',
            action='store_true',
            dest='shareholder_pk',
            default=False,
            help='provide single shareholder to generate stmts for',
        )

    def handle(self, *args, **options):
        for pk in options.get('company_pk', []):
            obj = Company.objects.filter(pk=pk).first()
            if obj is None:
                error_message = _(
                    'Could not find Company with id {}! Skipping...')
                self.stdout.write(error_message.format(pk))
                continue

            if options.get('shareholder_pk', []):
                shareholder = Shareholder.objects.get(
                    pk=options.get('shareholder_pk')[0])
            else:
                shareholder = None

            self._generate_report(obj, shareholder)

    def _generate_report(self, company, shareholder=None):
        today = now().date()
        report = company.shareholderstatementreport_set.get_or_create(
            report_date=today)
        report = report[0]

        if shareholder:
            if report.shareholderstatement_set.filter(user=shareholder.user):
                report.shareholderstatement_set.filter(
                    user=shareholder.user).delete()
            report._create_shareholder_statement_for_user(shareholder.user)
        else:
            report.shareholderstatement_set.all().delete()
            report.generate_statements(send_notify=False)
