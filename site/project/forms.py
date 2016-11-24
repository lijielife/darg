#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from registration.forms import (RegistrationFormTermsOfService,
                                RegistrationFormUniqueEmail)


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
        self.fields['tos'].widget.attrs['class'] = 'checkbox'
        return res
