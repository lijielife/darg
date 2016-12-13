#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from django.core.management.base import BaseCommand, CommandError

from utils.import_backends import IMPORT_BACKENDS


class Command(BaseCommand):
    help = 'Imports data into a companies captable'
    missing_args_message = 'Please provide company ID and filename to import'

    def _notice(self, msg):
        """
        shortcut to write to stdout
        """
        self.stdout.write(msg)

    def _success(self, msg):
        """
        shortcut to write to stdout
        """
        self.stdout.write(self.style.SUCCESS(msg))

    def _error(self, msg):
        """
        shortcut to write to stdout
        """
        self.stdout.write(self.style.ERROR(msg))

    def _get_file(self, filename):
        """
        checks file and returns file obj
        """
        if os.path.isfile(filename):
            return filename

        self._error('cannot read file {}'.format(filename))

    def _detect_backend(self, filename):
        """
        identify backend and return instance of it

        `f` is a file obj
        """
        for backend in IMPORT_BACKENDS:
            try:
                backend = backend(filename)
                return backend
            except ValueError:
                pass

        raise CommandError('No matching import backend detected')

    def add_arguments(self, parser):
        parser.add_argument('company_pk', nargs='+', type=int)
        parser.add_argument('file', nargs='+', type=str)

    def handle(self, *args, **options):
        """
        main call for management command. prepares data and sends it to backend
        """
        self._notice(
            'attempting import for company id "{}" from "{}"'.format(
                options['company_pk'][0], options['file'][0]))

        filename = self._get_file(options['file'][0])
        backend = self._detect_backend(filename)
        count = backend.import_from_file(options['company_pk'][0]) or 0

        self._success('Successfully imported {} data sets'.format(count))
