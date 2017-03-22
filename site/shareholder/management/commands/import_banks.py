#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from django.core.management.base import BaseCommand, CommandError

from shareholder.import_backends import SwissBankImportBackend

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'import latest swiss bank list'

    def handle(self, *args, **options):
        """
        main call for management command. prepares data and sends it to backend
        """
        try:
            logger.info('fetch swiss banks list ...')
            SwissBankImportBackend().update()
        except Exception as e:
            raise CommandError('Company reset failed with "{}"'.format(e))
