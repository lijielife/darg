
from django.db.models import ForeignKey
from model_mommy import mommy, random_gen


class AddressTestMixin(object):  # pragma: nocover

    def add_address(self, instance, save=True):
        """
        add required fields for valid address (REQUIRED_ADDRESS_FIELDS)
        """

        if not hasattr(instance, 'REQUIRED_ADDRESS_FIELDS'):
            return

        for fieldname in instance.REQUIRED_ADDRESS_FIELDS:
            field = instance._meta.get_field(fieldname)
            if isinstance(field, ForeignKey):
                val = mommy.make(
                    instance._meta.get_field(fieldname).related_model)
            else:
                val = random_gen.gen_string(10)
            setattr(instance, fieldname, val)

        if save:
            instance.save()
