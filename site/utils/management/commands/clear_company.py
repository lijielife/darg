#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError

from shareholder.models import Company


class Command(BaseCommand):
    help = 'resets a company to post registration state'
    missing_args_message = 'Please provide company PK'

    def add_arguments(self, parser):
        parser.add_argument('company_pk', nargs='+', type=int)

    def handle(self, *args, **options):
        """
        main call for management command. prepares data and sends it to backend
        """
        try:
            company = Company.objects.get(pk=options['company_pk'][0])
            for shareholder in company.shareholder_set.all():
                if shareholder.user.shareholder_set.count() < 2:
                    shareholder.user.delete()
                shareholder.delete()
            company.optionplan_set.all().delete()

        except Exception as e:
            raise CommandError('Company reset failed with "{}"'.format(e))
