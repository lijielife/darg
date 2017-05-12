#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.apps import AppConfig


class ShareholderAppConfig(AppConfig):
    name = 'shareholder'

    def ready(self):
        from shareholder import signals
