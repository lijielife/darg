#!/usr/bin/python
# -*- coding: utf-8 -*-

from project.celery import app

from shareholder.import_backends import SwissBankImportBackend


@app.task
def update_banks_from_six():
    """
    regularly update swiss banks database with data from six
    """
    SwissBankImportBackend().update()
