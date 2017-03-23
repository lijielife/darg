#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os

import celery
import raven
from celery.schedules import crontab
from django.core.management import call_command
from raven.contrib.celery import register_logger_signal, register_signal

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings.base')

# load after settings module being set:
from django.conf import settings  # noqa


class Celery(celery.Celery):

    def on_configure(self):
        client = raven.Client(settings.RAVEN_CONFIG.get('dsn'))

        # register a custom filter to filter out duplicate logs
        register_logger_signal(client)

        # hook into the Celery error handler
        register_signal(client)


app = Celery(__name__)

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task
def backup():
    call_command('dbbackup')
    call_command('mediabackup')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from shareholder.tasks import update_banks_from_six
    sender.add_periodic_task(
        crontab(hour=3, minute=0), backup.s())  # Nightly backups at 3AM
    sender.add_periodic_task(
        crontab(hour=4, minute=0, day_of_month=1), update_banks_from_six.s())
