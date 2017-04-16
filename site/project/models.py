#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.fields import AutoCreatedField, AutoLastModifiedField


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created_at`` and ``modified_at`` fields.

    taken from model_utils but added the '_at' suffix for field names
    """
    created_at = AutoCreatedField(_('created at'))
    modified_at = AutoLastModifiedField(_('modified at'))

    class Meta:
        abstract = True
