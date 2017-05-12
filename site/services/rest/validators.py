from django.utils.translation import ugettext_lazy as _

from rest_framework.exceptions import ValidationError


class DependentFieldsValidator:

    message = _(
        'The fields {field_names} must be empty together or contain values.')

    def __init__(self, fields):
        self.fields = fields

    def __call__(self, data):
        # validation pass only if either all fields have a value or none has
        bit = None
        for field in self.fields:
            if bit is not None and bit != (data.get(field) is None):
                raise ValidationError(self.message.format(
                    field_names=self.fields))

            bit = data.get(field) is None

    def set_context(self, serializer):
        """
        This hook is called by the serializer instance,
        prior to the validation call being made.
        """
        # Determine the existing instance, if this is an update operation.
        self.instance = getattr(serializer, 'instance', None)
