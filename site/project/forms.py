#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from rest_framework.authtoken.models import Token

from registration.forms import (RegistrationFormTermsOfService,
                                RegistrationFormUniqueEmail)
from shareholder.models import UserProfile

logger = logging.getLogger(__name__)


class RegistrationForm(RegistrationFormTermsOfService,
                       RegistrationFormUniqueEmail):
    """
    merge forms to have unique email and ToS checkbox in registration
    """
    def __init__(self, *args, **kwargs):
        """
        create form obj
        """
        res = super(RegistrationForm, self).__init__(*args, **kwargs)
        # add url to ToS string in form
        self.fields.get('tos').label = mark_safe(_(
            'I have read and agree to the '
            '<a href="http://www1.das-aktienregister.ch/agb" '
            'alt="Darg Terms of Service" target="_blank" class="link tos">'
            'Terms of Service'
            '</a>'
        ))
        return res

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=commit)

        # add api token
        Token.objects.create(user=user)

        # add user profile
        profile = UserProfile.objects.create(user=user)
        profile.tnc_accepted = True
        profile.save()

        # user legal type detection
        if user.first_name == settings.COMPANY_INITIAL_FIRST_NAME:
            profile.legal_type = 'C'
            profile.save()

        return user
