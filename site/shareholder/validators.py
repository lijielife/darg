#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf import settings
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
        self.security_share_count()
        self.company_share_count()
        self.company_has_initial_position()
        self.shareholder_mailing_type()  # must be last

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

    def security_share_count(self):
        """
        each security.count must match whats owned by shareholders
        """
        for security in self.company.security_set.all():
            if security.count != security.calculate_count():
                raise ValidationError(
                    _('Security count does not match transactions count: {}')
                    .format(security)
                )

    def company_share_count(self):
        """
        company share count must match whats owned by shareholders
        """
        count = 0
        for security in self.company.security_set.all():
            count += security.calculate_count()

        if count != self.company.share_count:
            raise ValidationError(
                _('Company share count "{}" does not match security count from '
                  'positions "{}"').format(self.company.share_count, count))

    def shareholder_mailing_type(self):
        """
        shareholder mailing type must not be unzustellbar
        """
        # local import to avoid circular import
        from shareholder.models import MAILING_TYPES  # noqa
        qs = self.company.shareholder_set.filter(
            mailing_type=MAILING_TYPES[0][0]
        )

        if (qs.exists()):
            raise ValidationError(
                _('Address of some shareholders is not reachable via postal '
                  'mail: {}').format(qs.values_list('user__email', 'user__pk')))

    def company_has_initial_position(self):
        """
        company shareholder has first cap increase/founding position without
        seller
        """
        s = self.company.get_company_shareholder()
        for security in self.company.security_set.all():
            qs = s.buyer.filter(security=security).order_by('bought_at')
            if (qs.exists() and qs[0].seller is None and
                    qs[0].bought_at <= security.position_set.order_by(
                        'bought_at'
                    ).first().bought_at):
                return

            raise ValidationError(
                _('Initial position for security {} is invalid').format(
                    security))


def validate_remote_email_id(value):
    sep = getattr(settings, 'REMOTE_EMAIL_SEPARATOR', '$')
    if value.count(sep) == 1:
        # check if there are values besides the separator
        provider, email_id = value.split(sep)
        if provider and email_id:
            return

    raise ValidationError(
        _('Enter a valid string of format [provider]{sep}[EMAIL_ID]').format(
            **dict(sep=sep)))
