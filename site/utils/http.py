#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib.sites.models import Site


def url_with_domain(path):
    return 'https://%s%s' % (Site.objects.get_current().domain,
                             path)
