# coding=utf-8

import mimetypes
import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.timezone import now

import requests

from .conf import pingen_settings
from .models import APICall


PINGEN_API_URL = getattr(settings, 'PINGEN_API_URL',
                         settings.DEBUG and pingen_settings.API_TEST_URL or
                         pingen_settings.API_LIVE_URL)


class Pingen(object):

    def __init__(self, token=None):
        self.token = token or getattr(settings, 'PINGEN_API_TOKEN')
        if not self.token:
            raise ImproperlyConfigured('Missing PINGEN_API_TOKEN in settings')

    def get_api_url(self, path, include_token=True):
        """
        return complete url

        Keyword agruments:
        include_token -- with appended token (default: True)
        """
        if not path.startswith('/'):
            path = '/' + path

        url = u'{}{}/'.format(PINGEN_API_URL.rstrip('/'), path.rstrip('/'))

        if include_token:
            url += u'token/{}/'.format(self.token)

        return url

    def upload_document(self, doc, send=None, speed=None, color=None,
                        duplex=None, rightaddress=None, envelope=None):
        """
        upload a document (PDF or ZIP)
        """

        if not doc or not os.path.isfile(doc):
            raise ValueError(u'Could not find file: {}'.format(doc))

        filename, ext = os.path.splitext(doc)

        mimetype = mimetypes.MimeTypes().guess_type(doc)[0]
        # NOTE: very simplistic fallback (not bullet proof at all!)
        mimetype = mimetype or 'application/{}'.format(ext.lstrip('.'))

        files = dict(
            file=(
                filename + ext,
                open(doc, 'rb'),
                mimetype
            )
        )
        data = dict(
            send=send is not None and send or pingen_settings.SEND_ON_UPLOAD,
            speed=speed is not None and speed or pingen_settings.SEND_SPEED,
            color=color is not None and color or pingen_settings.SEND_COLOR,
            duplex=(
                duplex is not None and duplex or pingen_settings.SEND_DUPLEX),
            rightaddress=(rightaddress is not None and rightaddress
                          or pingen_settings.RIGHT_ADDRESS),
            envelope=(envelope is not None and envelope
                      or pingen_settings.SEND_ENVELOPE)
        )

        # api call
        start = now()
        url_path = 'document/upload'
        url = self.get_api_url(url_path)
        timeout = pingen_settings.API_TIMEOUT
        res = requests.post(url, json=data, files=files, timeout=timeout)
        end = now()

        if res.status_code == 200:
            res_data = res.json()
            error = res_data.get('error', False)
            success = not error and res_data.get('id') or False
        else:
            success = False

        # store call
        APICall.objects.create(
            url=self.get_api_url(url_path, include_token=False),
            method='post',
            request_headers=res.request.headers,
            request_data=data,
            files=doc,
            started_at=start,
            ended_at=end,
            duration=end - start,
            status_code=res.status_code,
            response_headers=res.headers,
            response_text=res.text
        )

        return success
