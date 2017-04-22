#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib.sites.models import Site


def get_file_content_as_string(response):
    content = b''.join(response.streaming_content)
    return content


def url_with_domain(path):
    return 'https://%s%s' % (Site.objects.get_current().domain,
                             path)
