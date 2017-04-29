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
    from reports.tasks import prerender_reports
    sender.add_periodic_task(
        crontab(hour=3, minute=0), backup.s())  # Nightly backups at 3AM

    # shareholder tasks
    from shareholder.tasks import (send_statement_generation_operator_notify,
                                   send_statement_report_operator_notify,
                                   generate_statements_report,
                                   fetch_statement_email_opened_mandrill,
                                   send_statement_letters)
    sender.add_periodic_task(
        crontab(hour=9, minute=0),  # every morning at 9AM
        send_statement_generation_operator_notify.s()
    )
    sender.add_periodic_task(
        crontab(hour=9, minute=0),  # every morning at 9AM
        send_statement_report_operator_notify.s()
    )
    sender.add_periodic_task(
        crontab(hour=10, minute=0),  # every morning at 10AM
        generate_statements_report.s()
    )
    sender.add_periodic_task(
        crontab(hour=5, minute=0),  # every morning at 5AM
        fetch_statement_email_opened_mandrill.s()
    )
    sender.add_periodic_task(
        crontab(hour=11, minute=0),  # every morning at 11AM
        send_statement_letters.s()
    )
    sender.add_periodic_task(
        crontab(hour=4, minute=0, day_of_month=1), update_banks_from_six.s())
    sender.add_periodic_task(
        crontab(hour=2, minute=0), prerender_reports.s())
