#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core import mail
from django.core.urlresolvers import reverse
from django.test import Client, RequestFactory, TestCase
from django.utils.translation import ugettext as _
from model_mommy import mommy

from project.generators import (OperatorGenerator, OptionTransactionGenerator,
                                PositionGenerator, ShareholderGenerator,
                                UserGenerator, DEFAULT_TEST_DATA)
from project.tests.mixins import (MoreAssertsTestCaseMixin,
                                  StripeTestCaseMixin, SubscriptionTestMixin)
from shareholder.models import ShareholderStatement, ShareholderStatementReport
from shareholder.tests.mixins import StatementTestMixin
from shareholder.views import ShareholderView
from utils.session import add_company_to_session


class BaseViewTestCase(StripeTestCaseMixin, SubscriptionTestMixin, TestCase):

    def setUp(self):
        super(BaseViewTestCase, self).setUp()

        self.client = Client()
        self.shareholder1 = ShareholderGenerator().generate()
        self.company = self.shareholder1.company
        self.operator = OperatorGenerator().generate(company=self.company)
        self.operator2 = OperatorGenerator().generate()
        self.shareholder2 = ShareholderGenerator().generate()
        self.position1 = PositionGenerator().generate(buyer=self.shareholder1)
        self.position2 = PositionGenerator().generate(buyer=self.shareholder2)
        self.optiontransaction1 = OptionTransactionGenerator().generate(
            buyer=self.shareholder1)
        self.optiontransaction2 = OptionTransactionGenerator().generate(
            buyer=self.shareholder2)
        self.optionplan = self.optiontransaction1.option_plan

        self.statement_report = mommy.make(
            ShareholderStatementReport, company=self.shareholder1.company)
        self.statement = mommy.make(ShareholderStatement,
                                    user=self.shareholder1.user,
                                    pdf_file='example.pdf',
                                    report=self.statement_report)

        # add company subscription
        self.add_subscription(self.company)

        self.shareholder1_url = reverse('shareholder',
                                        kwargs={'pk': self.shareholder1.pk})


class DownloadTestCase(MoreAssertsTestCaseMixin, SubscriptionTestMixin,
                       TestCase):

    def _get_attachment_content(self, idx=None):
        """ from email with idx inside mail.outbox, get the first attachments
        string content
        """
        msgs = [msg for msg in mail.outbox if msg.attachments]
        msg = msgs[idx or 0]
        attn = msg.attachments[0]
        return attn[0], attn[1]

    def setUp(self):
        self.client = Client()

    def test_option_pdf(self):
        """ test printable certificate """
        ot = OptionTransactionGenerator().generate()
        company = ot.option_plan.company
        # run test
        response = self.client.get(
            reverse('option_pdf', kwargs={"option_id": ot.pk}))

        # not logged in user
        self.assertEqual(response.status_code, 302)

        # login and retest
        user = UserGenerator().generate()
        OperatorGenerator().generate(user=user, company=company)
        self.add_subscription(company)
        is_loggedin = self.client.login(username=user.username,
                                        password=DEFAULT_TEST_DATA['password'])
        self.assertTrue(is_loggedin)
        # was 53
        with self.assertLessNumQueries(78):
            response = self.client.get(
                reverse('option_pdf', kwargs={"option_id": ot.pk}))

        # assert response code
        self.assertEqual(response.status_code, 200)
        # assert proper csv
        content = response.content
        self.assertTrue(content.startswith('%PDF'))
        self.assertTrue(content.endswith('EOF\n'))

    def test_position_option_pdf(self):
        """ test printable certificate """
        pos = PositionGenerator().generate()
        company = pos.buyer.company
        # run test
        response = self.client.get(
            reverse('position_option_pdf', kwargs={"option_id": pos.pk}))

        # not logged in user
        self.assertEqual(response.status_code, 302)

        # login and retest
        user = UserGenerator().generate()
        OperatorGenerator().generate(user=user, company=company)
        self.add_subscription(company)
        is_loggedin = self.client.login(username=user.username,
                                        password=DEFAULT_TEST_DATA['password'])
        self.assertTrue(is_loggedin)
        # was 55
        with self.assertLessNumQueries(79):
            response = self.client.get(
                reverse('position_option_pdf', kwargs={"option_id": pos.pk}))

        # assert response code
        self.assertEqual(response.status_code, 200)
        # assert proper csv
        content = response.content
        self.assertTrue(content.startswith('%PDF-1'))
        self.assertTrue(content.endswith('EOF\n'))


class ShareholderViewTestCase(BaseViewTestCase):

    def setUp(self):
        super(ShareholderViewTestCase, self).setUp()

        self.factory = RequestFactory()
        self.view = ShareholderView()
        self.view.kwargs = {'pk': self.shareholder1.pk}
        request = self.factory.get(self.shareholder1_url)
        self.view.request = request
        add_company_to_session(self.client.session, self.shareholder1.company)
        self.view.request.session = self.client.session

    def test_get_statements(self):
        """ get statements for shareholder """
        self.assertEqual(list(self.view._get_statements().get('statements')),
                         [self.statement])

    def test_permissions(self):
        """
        test shareholder detail access check
        """
        self.client.force_login(self.operator.user)

        res = self.client.get(self.shareholder1_url)
        self.assertEqual(res.status_code, 200)

        res = self.client.get(reverse('shareholder',
                              kwargs={'pk': self.shareholder2.pk}))
        self.assertEqual(res.status_code, 302)  # redirect to login
        self.assertIn('login', res.url)

    def test_display(self):
        """ test display of certain content """

        self.client.force_login(self.operator.user)
        res = self.client.get(reverse('shareholder',
                              kwargs={'pk': self.shareholder1.pk}))
        self.assertEqual(res.status_code, 200)
        self.assertIn(_('Depot Statements'), res.content.decode('utf-8'))

    def test_enrich_security_objects(self):
        """ obj get addtional data attached before display """
        context_dict = self.view._enrich_security_objects()
        for sec in context_dict['securities']:
            self.assertIsNotNone(sec.count)
            self.assertIsNotNone(sec.options_count)

    def test_shareholder_detail(self):
        """ test detail view access for shareholder user """

        shareholder = ShareholderGenerator().generate()

        response = self.client.force_login(shareholder.user)

        response = self.client.get(
            reverse("shareholder", args=(shareholder.id,)))

        self.assertEqual(response.status_code, 200)


class PositionViewTestCase(BaseViewTestCase):

    def test_view(self):
        """
        test shareholder detail view
        """
        self.client.force_login(self.operator.user)

        res = self.client.get(reverse('position',
                              kwargs={'pk': self.position1.pk}))
        self.assertEqual(res.status_code, 200)

        res = self.client.get(reverse('position',
                              kwargs={'pk': self.position2.pk}))
        self.assertEqual(res.status_code, 302)  # redirect to login
        self.assertIn('login', res.url)


class OptionTransactionViewTestCase(BaseViewTestCase):

    def test_view(self):
        """
        test shareholder detail view
        """
        self.client.force_login(self.operator.user)

        res = self.client.get(reverse('optiontransaction',
                              kwargs={'pk': self.optiontransaction1.pk}))
        self.assertEqual(res.status_code, 200)

        res = self.client.get(reverse('optiontransaction',
                              kwargs={'pk': self.optiontransaction2.pk}))
        self.assertEqual(res.status_code, 302)  # redirect to login
        self.assertIn('login', res.url)


class PositionsViewTestCase(BaseViewTestCase):

    def test_view(self):
        """
        test shareholder detail view
        """
        self.url = reverse('positions')
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 302)

        self.client.force_login(self.operator.user)
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 200)

        self.client.force_login(self.operator2.user)
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 302)


class OptionTransactionsViewTestCase(BaseViewTestCase):

    def test_view(self):
        """
        test shareholder detail view
        """
        self.url = reverse('options')
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 302)

        self.client.force_login(self.operator.user)
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 200)

        self.client.force_login(self.operator2.user)
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 302)


class OptionPlanViewTestCase(BaseViewTestCase):

    def test_view(self):
        """
        test shareholder detail view
        """
        self.url = reverse('optionplan', kwargs={'pk': self.optionplan.pk})
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 302)

        self.client.force_login(self.operator.user)
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 200)

        self.client.force_login(self.operator2.user)
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 302)


# ----- STATEMENT VIEW TESTS
class StatementListViewTestCase(StatementTestMixin, BaseViewTestCase):

    def test_get(self):
        """ shareholder can view list of statements for him """

        response = self.client.get(reverse('statements'))
        self.assertEqual(response.status_code, 302)

        self.client.force_login(self.shareholder.user)
        response = self.client.get(reverse('statements'))
        self.assertEqual(response.status_code, 200)


class StatementReportViewTestCase(StatementTestMixin, BaseViewTestCase):

    def test_get(self):
        """ shareholder can view list of statements for him """

        response = self.client.get(reverse('statement_report',
                                   kwargs={'pk': self.report.pk}))
        self.assertEqual(response.status_code, 302)

        self.client.force_login(self.operator.user)
        response = self.client.get(reverse('statement_report',
                                   kwargs={'pk': self.report.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.statement.get_pdf_download_url(),
                      response.content.decode('utf-8'))
        # self.report.get_pdf_download_url inside?
        self.assertIn('allstatements/download/pdf',
                      response.content.decode('utf-8'))


class StatementDownloadPDFViewTestCase(StatementTestMixin, BaseViewTestCase):

    def test_get(self):
        """ shareholder can view list of statements for him """

        response = self.client.get(self.statement.get_pdf_download_url())
        self.assertEqual(response.status_code, 302)

        self.client.force_login(self.shareholder.user)
        response = self.client.get(self.statement.get_pdf_download_url())
        self.assertEqual(response.status_code, 200)

        self.client.force_login(self.operator.user)
        response = self.client.get(self.statement.get_pdf_download_url())
        self.assertEqual(response.status_code, 200)


class StatementReportDownloadPDFViewTestCase(StatementTestMixin,
                                             BaseViewTestCase):

    def test_get(self):
        """ shareholder can view list of statements for him """

        response = self.client.get(self.report.get_pdf_download_url())
        self.assertEqual(response.status_code, 302)

        self.client.force_login(self.shareholder.user)
        response = self.client.get(self.report.get_pdf_download_url())
        self.assertEqual(response.status_code, 404)

        self.client.force_login(self.operator.user)
        response = self.client.get(self.report.get_pdf_download_url())
        self.assertEqual(response.status_code, 200)
