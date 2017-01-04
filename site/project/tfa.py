#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
file to store string to be translated for tfa/two factor auth inside the project
"""
# from http://bit.ly/2iCCcRS
prompts = {
    # Translators: should be a language supported by Twilio,
    # see http://bit.ly/187I5cr
    'press_a_key': _('Hi, this is %(site_name)s calling. Press any key '
                     'to continue.'),

    # Translators: should be a language supported by Twilio,
    # see http://bit.ly/187I5cr
    'token': _('Your token is %(token)s. Repeat: %(token)s. Good bye.'),

    # Translators: should be a language supported by Twilio,
    # see http://bit.ly/187I5cr
    'no_input': _('You didn\'t press any keys. Good bye.')
}
