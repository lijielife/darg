#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class Validator(object):
    """
    common validation logic here
    """
    errors = []  # becomes list of error msgs

    def __init__(self, company):
        self.company = company

    def is_valid(self):
        raise NotImplementedError()


class ShareRegisterValidator(Validator):
    """
    giant suite to validate if a share registers data is fully valid
    """

    def is_valid(self):
        """
        entry point to have the validator do its job
        """
        self.has_operator()
        self.shareholders_have_users()

    def has_operator(self):
        """
        does the company have an operator?
        """
        try:
            self.company.operator_set.all()[0]
            return True
        except IndexError:
            raise ValidationError(_('No company operator existing.'))

    def shareholders_have_users(self):
        if not self.company.shareholder_set.filter(user__isnull=True).exists():
            return True

        shareholders = self.company.shareholder_set.filter(user__isnull=True)
        raise ValidationError(
            _('Shareholders have no user assigned: {}').format(
                [s.pk for s in shareholders]
            ))
