#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms

from djstripe.models import Plan


class PlanForm(forms.Form):
    """A form used when creating a Plan. copied over from djstripe 0.8
    after migration attempt to 1.0.0. its used in darg, but will disapper in
    djstripe 1.0+"""

    plan = forms.ModelChoiceField(queryset=Plan.objects.all())
