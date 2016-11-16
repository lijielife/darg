
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_remote_email_id(value):
    sep = getattr(settings, 'REMOTE_EMAIL_SEPARATOR', '$')
    print(value, sep)
    if value.count(sep) == 1:
        # check if there are values besides the separator
        provider, email_id = value.split(sep)
        if provider and email_id:
            return

    raise ValidationError(
        _('Enter a valid string of format [provider]{sep}[EMAIL_ID]').format(
            **dict(sep=sep)))
