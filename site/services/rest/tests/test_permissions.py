
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory

from rest_framework.views import APIView
from rest_framework.test import APITestCase

from project.generators import OperatorGenerator, UserGenerator
from project.tests.mixins import StripeTestCaseMixin, SubscriptionTestMixin

from ..permissions import IsOperatorPermission, HasSubscriptionPermission
from utils.session import add_company_to_session


class IsOperatorPermissionTestCase(APITestCase):

    def setUp(self):
        super(IsOperatorPermissionTestCase, self).setUp()

        self.factory = RequestFactory()
        self.permission = IsOperatorPermission()

    def test_has_permission(self):
        view = APIView()

        req = self.factory.get('/')
        req.user = AnonymousUser()

        # not authenticated
        self.assertFalse(self.permission.has_permission(req, view))

        req.user = UserGenerator().generate()
        # authenticated but no operator
        self.assertFalse(self.permission.has_permission(req, view))

        # add operator for user
        op = OperatorGenerator().generate(user=req.user)
        add_company_to_session(self.client.session, op.company)
        req.session = self.client.session
        # user is authenticated and operator
        self.assertTrue(self.permission.has_permission(req, view))


class HasSubscriptionPermissionTestCase(StripeTestCaseMixin,
                                        SubscriptionTestMixin, APITestCase):

    def setUp(self):
        super(HasSubscriptionPermissionTestCase, self).setUp()

        self.factory = RequestFactory()
        self.permission = HasSubscriptionPermission()
        self.operator = OperatorGenerator().generate()
        # steal session from client: http://stackoverflow.com/a/37307406/1270058
        self.session = self.client.session
        self.session['company_pk'] = self.operator.company.pk
        self.session.save()

    def test_has_permission(self):
        view = APIView()

        req = self.factory.get('/')
        req.user = AnonymousUser()

        # no company
        self.assertFalse(self.permission.has_permission(req, view))

        # add company operator
        req.user = self.operator.user
        req.session = self.session

        # no plan/subscription
        self.assertFalse(self.permission.has_permission(req, view))

        # add company subscription
        self.add_subscription(self.operator.company)

        # no subscription features on view defined
        self.assertTrue(self.permission.has_permission(req, view))

        view.subscription_features = ['foo']

        # feature not in plan features
        self.assertFalse(self.permission.has_permission(req, view))

        view.subscription_features = ['shareholders']

        plans = settings.DJSTRIPE_PLANS.copy()
        plans['test']['features']['shareholders'] = {}
        with self.settings(DJSTRIPE_PLANS=plans):
            self.assertTrue(self.permission.has_permission(req, view))

        view.action = 'bar'
        # view action has no validator
        self.assertTrue(self.permission.has_permission(req, view))

        plans['test']['features']['shareholders'] = {
            'max': 2,
            'validators': {
                'bar': [
                    'company.validators.features.'
                    'ShareholderCreateMaxCountValidator'
                ]
            }
        }
        with self.settings(DJSTRIPE_PLANS=plans):
            self.assertTrue(self.permission.has_permission(req, view))

        plans['test']['features']['shareholders']['max'] = 0
        with self.settings(DJSTRIPE_PLANS=plans):
            self.assertFalse(self.permission.has_permission(req, view))

    def test_get_object_permission(self):
        # TODO: add real tests after logic is determined in permission
        req = self.factory.get('/')
        req.session = self.session
        view = APIView()
        self.assertTrue(self.permission.has_object_permission(req, view))
