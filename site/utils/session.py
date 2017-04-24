#!/usr/bin/python
# -*- coding: utf-8 -*-

from shareholder.models import Company


def get_company_from_request(request, fail_silently=False):
    """
    returns company obj based on session key
    """
    if hasattr(request, 'session') and request.session.get('company_pk'):
        return Company.objects.get(pk=request.session.get('company_pk'))

    if fail_silently:
        return False

    raise ValueError('company_pk missing in session')


def add_company_to_session(session, company):

    session['company_pk'] = company.pk
    session.save()
