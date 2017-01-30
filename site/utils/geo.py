#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf import settings
from django_languages.languages import LANGUAGES
from django.utils.translation import gettext_lazy as _
from django.utils import translation

# used to map strings for countries to Country obj name strings during import
COUNTRY_MAP = {
    u'Schweiz': 'CH',
    u'Portugal': 'PT',
    u'<unbekannt>': '',
    u'England': 'GB',
    u'Spanien': 'ES',
    u'Deutschland': 'DE',
    u'USA': 'US',
}


def _get_language_iso_code(lang):

    for key, name in LANGUAGES:
        with translation.override(settings.LANGUAGE_CODE):
            if lang == _(name.encode('utf-8')):
                return key


# language translation strings to make langs from http://bit.ly/2hQAzTz
# translatable
_('German')
