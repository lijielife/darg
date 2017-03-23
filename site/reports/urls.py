#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from reports.views import IndexView


urlpatterns = [
    # web views
    url(r'^$', login_required(IndexView.as_view()), name='reports'),
 ]
