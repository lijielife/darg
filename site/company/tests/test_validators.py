from copy import copy

from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings

from model_mommy import random_gen

from project.generators import (CompanyGenerator, ShareholderGenerator,
                                SecurityGenerator)
from project.tests.mixins import StripeTestCaseMixin, SubscriptionTestMixin
from shareholder.tests.mixins import AddressTestMixin

from ..validators import CompanyEmailRequired, CompanyAddressRequired
from ..validators.base import BaseCompanyValidator
from ..validators.features import (ShareholderCountPlanValidator,
                                   SecurityCountPlanValidator,
                                   ShareholderCreateMaxCountValidator,
                                   SecurityCreateMaxCountValidator)


class CompanyEmailRequiredTestCase(TestCase):

    def setUp(self):
        super(CompanyEmailRequiredTestCase, self).setUp()

        company = CompanyGenerator().generate()
        self.validator = CompanyEmailRequired(company)

    def test_call(self):

        with self.assertRaises(ValidationError):
            self.validator()

        self.validator.company.email = random_gen.gen_string(20)

        with self.assertRaises(ValidationError):
            self.validator()

        self.validator.company.email = random_gen.gen_email()

        self.assertIsNone(self.validator())


class CompanyAddressRequiredTestCase(AddressTestMixin, TestCase):

    def setUp(self):
        super(CompanyAddressRequiredTestCase, self).setUp()

        company = CompanyGenerator().generate()
        self.validator = CompanyAddressRequired(company)

    def test_call(self):

        with self.assertRaises(ValidationError):
            self.validator()

        self.add_address(self.validator.company)

        self.assertIsNone(self.validator())

        setattr(
            self.validator.company,
            self.validator.company.REQUIRED_ADDRESS_FIELDS[0],
            None
        )

        with self.assertRaises(ValidationError):
            self.validator()


class BaseCompanyValidatorTestCase(TestCase):

    def setUp(self):
        super(BaseCompanyValidatorTestCase, self).setUp()

        self.validator_class = BaseCompanyValidator
        self.company = CompanyGenerator().generate()

    def test_init(self):

        with self.assertRaises(ValueError):
            self.validator_class(None)

        validator = self.validator_class(self.company)
        self.assertEqual(validator.company, self.company)

    def test_raise_exception(self):

        validator = self.validator_class(self.company)
        error_message = random_gen.gen_string(10)
        with self.assertRaises(ValidationError) as ex:
            validator.raise_execption(error_message)
            self.assertEqual(ex.message, error_message)  # pragma: no cover
            self.assertIsNone(ex.code)  # pragma: no cover

        code = random_gen.gen_integer()
        with self.assertRaises(ValidationError) as ex:
            validator.raise_execption(error_message, code)
            self.assertEqual(ex.message, error_message)  # pragma: no cover
            self.assertEqual(ex.code, code)  # pragma: no cover

    def test_raise_error(self):

        validator = self.validator_class(self.company)
        error_message = random_gen.gen_string(10)
        with self.assertRaises(ValidationError) as ex:
            validator.raise_error(error_message)
            self.assertEqual(ex.message, error_message)  # pragma: no cover
            self.assertIsNone(ex.code)  # pragma: no cover

        code = random_gen.gen_integer()
        with self.assertRaises(ValidationError) as ex:
            validator.raise_error(error_message, code)
            self.assertEqual(ex.message, error_message)  # pragma: no cover
            self.assertEqual(ex.code, code)  # pragma: no cover


class ShareholderCountPlanValidatorTestCase(TestCase):

    def setUp(self):
        super(ShareholderCountPlanValidatorTestCase, self).setUp()

        company = CompanyGenerator().generate()
        self.validator = ShareholderCountPlanValidator(company)

    def test_call(self):

        with self.assertRaises(ValueError):
            self.validator('')

        plan_name = settings.DJSTRIPE_PLANS.keys()[0]

        self.assertIsNone(self.validator(plan_name))

        MODIFIED_DJSTRIPE_PLANS = copy(settings.DJSTRIPE_PLANS)
        MODIFIED_DJSTRIPE_PLANS[plan_name]['features']['shareholders'] = {
            'max': 1
        }

        with self.settings(DJSTRIPE_PLANS=MODIFIED_DJSTRIPE_PLANS):
            self.assertIsNone(self.validator(plan_name))

            # add shareholder
            ShareholderGenerator().generate(company=self.validator.company)

            self.assertIsNone(self.validator(plan_name))

            # add another shareholder
            ShareholderGenerator().generate(company=self.validator.company)

            with self.assertRaises(ValidationError):
                self.validator(plan_name)


class SecurityCountPlanValidatorTestCase(TestCase):

    def setUp(self):
        super(SecurityCountPlanValidatorTestCase, self).setUp()

        company = CompanyGenerator().generate()
        self.validator = SecurityCountPlanValidator(company)

    def test_call(self):

        with self.assertRaises(ValueError):
            self.validator('')

        plan_name = settings.DJSTRIPE_PLANS.keys()[0]

        self.assertIsNone(self.validator(plan_name))

        MODIFIED_DJSTRIPE_PLANS = copy(settings.DJSTRIPE_PLANS)
        MODIFIED_DJSTRIPE_PLANS[plan_name]['features']['securities'] = {
            'max': 1
        }

        with self.settings(DJSTRIPE_PLANS=MODIFIED_DJSTRIPE_PLANS):
            self.assertIsNone(self.validator(plan_name))

            # add security
            SecurityGenerator().generate(company=self.validator.company)

            self.assertIsNone(self.validator(plan_name))

            # add another security
            SecurityGenerator().generate(company=self.validator.company)

            with self.assertRaises(ValidationError):
                self.validator(plan_name)


class ShareholderCreateMaxCountValidatorTestCase(StripeTestCaseMixin,
                                                 SubscriptionTestMixin,
                                                 TestCase):

    def setUp(self):
        super(ShareholderCreateMaxCountValidatorTestCase, self).setUp()

        company = CompanyGenerator().generate()
        self.validator = ShareholderCreateMaxCountValidator(company)

    @override_settings()
    def test_call(self):

        self.assertIsNone(self.validator())

        # add subscription
        self.add_subscription(self.validator.company)

        self.assertIsNone(self.validator())

        plan_name = self.validator.company.get_current_subscription_plan()

        MODIFIED_DJSTRIPE_PLANS = copy(settings.DJSTRIPE_PLANS)
        MODIFIED_DJSTRIPE_PLANS[plan_name]['features']['shareholders'] = {
            'max': 1
        }

        with self.settings(DJSTRIPE_PLANS=MODIFIED_DJSTRIPE_PLANS):
            self.assertIsNone(self.validator())

            # add shareholder
            ShareholderGenerator().generate(company=self.validator.company)

            with self.assertRaises(ValidationError):
                self.validator()


class SecurityCreateMaxCountValidatorTestCase(StripeTestCaseMixin,
                                              SubscriptionTestMixin, TestCase):

    def setUp(self):
        super(SecurityCreateMaxCountValidatorTestCase, self).setUp()

        company = CompanyGenerator().generate()
        self.validator = SecurityCreateMaxCountValidator(company)

    def test_call(self):

        self.assertIsNone(self.validator())

        # add subscription
        self.add_subscription(self.validator.company)

        self.assertIsNone(self.validator())

        plan_name = self.validator.company.get_current_subscription_plan()

        MODIFIED_DJSTRIPE_PLANS = copy(settings.DJSTRIPE_PLANS)
        MODIFIED_DJSTRIPE_PLANS[plan_name]['features']['securities'] = {
            'max': 1
        }

        self.assertIsNone(self.validator())

        # add security
        SecurityGenerator().generate(company=self.validator.company)

        with self.assertRaises(ValidationError):
            self.validator()
