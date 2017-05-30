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
    url(r'^company/(?P<company_id>[0-9]+)/download/transactions$',
        login_required(views.transactions_xls), name='transactions_xls'),
 ]
