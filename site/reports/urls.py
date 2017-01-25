#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import url

from reports.views import IndexView


urlpatterns = [
    # web views
    url(r'^$', IndexView.as_view(), name='reports'),  # reports overview
 ]
