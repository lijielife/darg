
from django.db.models import ForeignKey
from django.utils import timezone
from model_mommy import mommy, random_gen

from project.generators import (OperatorGenerator, PositionGenerator,
                                ShareholderGenerator)


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


class StatementTestMixin(object):

    def setUp(self):
        super(StatementTestMixin, self).setUp()
        self.company_shareholder = ShareholderGenerator().generate()
        self.shareholder = ShareholderGenerator().generate(
            company=self.company_shareholder.company)
        PositionGenerator().generate(
            buyer=self.shareholder, seller=None, count=100)
        self.company = self.shareholder.company
        self.add_subscription(self.company)
        self.report = self.company.shareholderstatementreport_set.create(
            report_date=timezone.now().date())
        self.report.generate_statements()
        self.operator = OperatorGenerator().generate(company=self.company)
        self.statement = self.shareholder.user.shareholderstatement_set.first()
