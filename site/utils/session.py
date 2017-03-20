#!/usr/bin/python
# -*- coding: utf-8 -*-

from shareholder.models import Company


def get_company_from_request(request):
    """
    returns company obj based on session key
    """
    if request.session.get('company_pk'):
        return Company.objects.get(pk=request.session.get('company_pk'))

    raise ValueError('company_pk missing in session')
