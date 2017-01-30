#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q

from shareholder.models import Company, Position, OptionTransaction

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'resets a company to post registration state'
    missing_args_message = 'Please provide company PK'

    def add_arguments(self, parser):
        parser.add_argument('company_pk', nargs='+', type=int)
        parser.add_argument(
            '--keep-operator',
            action='store_true',
            dest='keep_operator',
            default=False,
            help='Do not delete operator roles',
        )

    def handle(self, *args, **options):
        """
        main call for management command. prepares data and sends it to backend
        """
        try:
            logger.info('fetch company...')
            company = Company.objects.get(pk=options['company_pk'][0])
            logger.info('delete shareholders and assigned users...')
            for shareholder in company.shareholder_set.all():
                if shareholder.user.shareholder_set.count() < 2:
                    shareholder.user.userprofile.delete()
                    shareholder.user.delete()
                shareholder.delete()
            logger.info('delete optionplans and assigned transactions...')
            company.optionplan_set.all().delete()
            if not options['keep_operator']:
                company.operator_set.all().delete()
            company.security_set.all().delete()

            print('check: {} shareholders, {} optionplans, {} positions,'
                        '{} optiontransactions, {} securities, '
                        '{} operators'.format(
                            company.shareholder_set.count(),
                            company.optionplan_set.count(),
                            Position.objects.filter(
                                Q(buyer__company=company) | Q(seller__company=company)
                            ).count(),
                            OptionTransaction.objects.filter(
                                Q(buyer__company=company) | Q(seller__company=company)
                            ).count(),
                            company.security_set.count(),
                            company.operator_set.count(),
                        )
                )

        except Exception as e:
            raise CommandError('Company reset failed with "{}"'.format(e))
