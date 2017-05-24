#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from reports import views


urlpatterns = [
    # web views
    url(r'^$', login_required(views.IndexView.as_view()), name='reports'),
    url(r'^(?P<report_id>[0-9]+)/download$',
        login_required(views.report_download), name='download'),
    url(r'^company/(?P<company_id>[0-9]+)/download/contacts$',
        login_required(views.contacts_csv), name='contacts_csv'),
    url(r'^company/(?P<company_id>[0-9]+)/download/transactions$',
        login_required(views.transactions_csv), name='transactions_csv'),
    url(r'^company/(?P<company_id>[0-9]+)/download/vested$',
        login_required(views.vested_csv), name='vested_csv'),
    url(r'^company/(?P<company_id>[0-9]+)/download/printed_certificates_csv$',
        login_required(views.printed_certificates_csv),
        name='printed_certificates_csv'),
 ]
