#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from reports.views import IndexView, report_download


urlpatterns = [
    # web views
    url(r'^$', login_required(IndexView.as_view()), name='reports'),
    url(r'^(?P<report_id>[0-9]+)/download$', report_download, name='download'),
 ]
