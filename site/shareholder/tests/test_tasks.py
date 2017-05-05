
import json
import os
import time

import mock
from django.conf import settings
from django.test import TestCase, override_settings
from django.utils.timezone import now, timedelta
from model_mommy import mommy, random_gen

from project.generators import (CompanyGenerator, OperatorGenerator,
                                ShareholderGenerator)
from project.tests.mixins import (FakeResponseMixin, StripeTestCaseMixin,
                                  SubscriptionTestMixin)

from ..models import ShareholderStatement, ShareholderStatementReport
from ..tasks import (_context_email_defaults,
                     fetch_statement_email_opened_mandrill,
                     generate_statements_report, send_statement_email,
                     send_statement_generation_operator_notify,
                     send_statement_letter, send_statement_letters,
                     send_statement_report_operator_notify,
                     update_order_cache_task)
from .mixins import AddressTestMixin


class TasksHelperTestCase(TestCase):

    def test_context_email_defaults(self):
        with self.settings(VERSION='0.0.0'):
            context = _context_email_defaults()
            self.assertIn('domain', context)
            self.assertIn('VERSION', context)
            self.assertEqual(context.get('VERSION'), 'v0.0.0')


class TasksTestCase(AddressTestMixin, FakeResponseMixin, StripeTestCaseMixin,
                    SubscriptionTestMixin, TestCase):

    @override_settings(SHAREHOLDER_STATEMENT_OPERATOR_NOTIFY_DAYS=0)
    @mock.patch('shareholder.tasks.render_pdf')
    @mock.patch('shareholder.tasks.EmailMultiAlternatives.send',
                return_value=1)
    @mock.patch('shareholder.tasks.EmailMessage.send', return_value=1)
    @mock.patch('shareholder.tasks.mail_admins')
    def test_send_statement_generation_operator_notify(self, mock_mail_admins,
                                                       mock_email_message_send,
                                                       mock_email_multi_send,
                                                       mock_render_pdf):
        company = CompanyGenerator().generate()
        company.is_statement_sending_enabled = True
        company.statement_sending_date = now().date()
        company.save()

        # no subscription
        send_statement_generation_operator_notify()
        mock_mail_admins.assert_not_called()
        mock_email_message_send.assert_not_called()
        mock_email_multi_send.assert_not_called()

        # add subscription
        self.add_subscription(company)

        # no operators
        send_statement_generation_operator_notify()
        mock_mail_admins.assert_called()
        mock_email_message_send.assert_not_called()
        mock_email_multi_send.assert_not_called()

        OperatorGenerator().generate(company=company)

        with self.settings(EMAIL_BACKEND='dummy'):
            send_statement_generation_operator_notify()
            mock_email_multi_send.assert_called()

        djrill_settings = {
            'EMAIL_BACKEND': 'djrill',
            'MANDRILL_SHAREHOLDER_STATEMENT_OPERATOR_NOTIFY_TEMPLATE': 'foo'
        }
        with self.settings(**djrill_settings):
            send_statement_generation_operator_notify()
            mock_email_message_send.assert_called()

        mock_mail_admins.reset_mock()
        mock_email_multi_send.reset_mock()

        mock_render_pdf.return_value = 'PDFCONTENT'
        with mock.patch('shareholder.tasks.'
                        'EmailMultiAlternatives.attach') as mock_attach:
            send_statement_generation_operator_notify()
            mock_attach.assert_called()
            mock_attach.reset_mock()

            mock_render_pdf.side_effect = Exception
            send_statement_generation_operator_notify()
            mock_attach.assert_not_called()

        mock_mail_admins.assert_not_called()
        mock_email_multi_send.return_value = 0
        send_statement_generation_operator_notify()
        mock_mail_admins.assert_called()

    @override_settings(SHAREHOLDER_STATEMENT_REPORT_OPERATOR_NOTIFY_DAYS=0)
    @mock.patch('shareholder.tasks.EmailMultiAlternatives.send',
                return_value=1)
    @mock.patch('shareholder.tasks.EmailMessage.send', return_value=1)
    @mock.patch('shareholder.tasks.mail_admins')
    def test_send_statement_report_operator_notify(self, mock_mail_admins,
                                                   mock_email_message_send,
                                                   mock_email_multi_send):
        company = CompanyGenerator().generate()
        mommy.make(ShareholderStatementReport, company=company,
                   report_date=now().date())

        send_statement_report_operator_notify()
        mock_mail_admins.assert_called()
        mock_mail_admins.reset_mock()

        OperatorGenerator().generate(company=company)

        with self.settings(EMAIL_BACKEND='dummy'):
            send_statement_report_operator_notify()
            mock_email_multi_send.assert_called()

        djrill_settings = {
            'EMAIL_BACKEND': 'djrill',
            'MANDRILL_SHAREHOLDER_STATEMENT_REPORT'
            '_OPERATOR_NOTIFY_TEMPLATE': 'foo'
        }
        with self.settings(**djrill_settings):
            send_statement_report_operator_notify()
            mock_email_message_send.assert_called()

        mock_email_multi_send.return_value = 0
        send_statement_report_operator_notify()
        mock_mail_admins.assert_called()

    @mock.patch(
        'shareholder.models.ShareholderStatementReport.generate_statements')
    def test_generate_statements_report(self, mock_generate_statements):

        company = CompanyGenerator().generate()
        company.is_statement_sending_enabled = True
        company.statement_sending_date = now().date()
        company.save()

        # no subscription
        generate_statements_report()
        mock_generate_statements.assert_not_called()

        # add subscription
        self.add_subscription(company)

        generate_statements_report()
        mock_generate_statements.assert_called()

    @mock.patch('shareholder.tasks.EmailMultiAlternatives.send',
                return_value=1)
    @mock.patch('shareholder.tasks.EmailMessage.send', return_value=1)
    @mock.patch('shareholder.tasks.send_mail')
    def test_send_statement_email(self, mock_send_mail,
                                  mock_email_message_send,
                                  mock_email_multi_alternatives_send):

        self.assertFalse(send_statement_email(0))

        statement = mommy.make(ShareholderStatement, pdf_file='example.pdf')

        # no user email
        self.assertFalse(statement.user.email)
        self.assertFalse(send_statement_email(statement.pk))
        mock_send_mail.assert_called_once()
        mock_send_mail.reset_mock()

        statement.user.email = random_gen.gen_email()
        statement.user.save()

        # pdf file is no file
        self.assertFalse(os.path.isfile(statement.pdf_file))
        self.assertFalse(send_statement_email(statement.pk))
        mock_send_mail.assert_called_once()
        mock_send_mail.reset_mock()

        statement.pdf_file = os.path.join(
            os.path.dirname(__file__), 'files', 'example.pdf'
        )
        statement.save()

        with self.settings(MANDRILL_SHAREHOLDER_STATEMENT_TEMPLATE=None):
            self.assertIsNone(statement.email_sent_at)
            self.assertTrue(send_statement_email(statement.pk))
            statement.refresh_from_db()
            self.assertIsNotNone(statement.email_sent_at)
            mock_email_multi_alternatives_send.assert_called_once()

        statement.email_sent_at = None
        statement.save()

        with self.settings(MANDRILL_SHAREHOLDER_STATEMENT_TEMPLATE='foo',
                           EMAIL_BACKEND='djrill'):
            self.assertTrue(send_statement_email(statement.pk))
            statement.refresh_from_db()
            self.assertIsNotNone(statement.email_sent_at)
            mock_email_message_send.assert_called_once()
            self.assertFalse(statement.remote_email_id)

            with mock.patch('shareholder.tasks.EmailMessage') as mock_message:
                remote_id = random_gen.gen_uuid().hex
                mandrill_response_mock = mock.PropertyMock(
                    return_value=[dict(_id=remote_id)])
                type(mock_message.return_value).mandrill_response = (
                    mandrill_response_mock)

                self.assertTrue(send_statement_email(statement.pk))
                statement.refresh_from_db()
                self.assertIn(remote_id, statement.remote_email_id)
                self.assertIn('mandrill', statement.remote_email_id)

    @override_settings(SHAREHOLDER_STATEMENT_EMAIL_OPENED_DAYS=2)
    @override_settings(MANDRILL_API_KEY='mandrill_key')
    @mock.patch('shareholder.tasks.requests')
    def test_fetch_statement_email_opened_mandrill(self, mock_requests):

        mock_requests.get = mock.Mock()
        self.fake_response_content = json.dumps(dict())
        mock_requests.get.return_value = self.get_fake_response('get')

        statement = mommy.make(ShareholderStatement, pdf_file='example.pdf')

        fetch_statement_email_opened_mandrill()
        mock_requests.get.assert_not_called()

        statement.email_sent_at = now() - timedelta(days=1)
        sep = getattr(settings, 'REMOTE_EMAIL_SEPARATOR', '$')
        remote_id = random_gen.gen_uuid().hex
        statement.remote_email_id = 'mandrill{}{}'.format(sep, remote_id)
        statement.save()

        fetch_statement_email_opened_mandrill()
        api_url = settings.MANDRILL_API_BASE_URL + 'messages/info.json'
        data = dict(key='mandrill_key', id=remote_id)
        mock_requests.get.assert_called_once_with(
            api_url, data=json.dumps(data))
        statement.refresh_from_db()
        self.assertIsNone(statement.email_opened_at)

        # state='sent' only
        self.fake_response_content = json.dumps(dict(state='sent'))
        mock_requests.get.return_value = self.get_fake_response('get')
        fetch_statement_email_opened_mandrill()
        statement.refresh_from_db()
        self.assertIsNone(statement.email_opened_at)

        # state='sent' and empty opens_detail
        self.fake_response_content = json.dumps(dict(
            state='sent',
            opens_detail=[]
        ))
        mock_requests.get.return_value = self.get_fake_response('get')
        fetch_statement_email_opened_mandrill()
        statement.refresh_from_db()
        self.assertIsNone(statement.email_opened_at)

        # state='sent' and opens_detail without 'ts'
        self.fake_response_content = json.dumps(dict(
            state='sent',
            opens_detail=[dict()]
        ))
        mock_requests.get.return_value = self.get_fake_response('get')
        fetch_statement_email_opened_mandrill()
        statement.refresh_from_db()
        self.assertIsNone(statement.email_opened_at)

        # valid response
        timestamp = int(time.mktime(now().timetuple()))
        self.fake_response_content = json.dumps(dict(
            state='sent',
            opens_detail=[dict(ts=timestamp)]
        ))
        mock_requests.get.return_value = self.get_fake_response('get')
        fetch_statement_email_opened_mandrill()
        statement.refresh_from_db()
        self.assertIsNotNone(statement.email_opened_at)
        self.assertEqual(time.mktime(statement.email_opened_at.timetuple()),
                         timestamp)

    @override_settings(PINGEN_API_TOKEN='123456789abcdef')
    @mock.patch('pingen.api.Pingen.upload_document', return_value=True)
    def test_send_statement_letter(self, mock_upload_document):

        self.assertFalse(send_statement_letter(0))

        company = CompanyGenerator().generate()
        report = mommy.make(ShareholderStatementReport, company=company)
        statement = mommy.make(ShareholderStatement, report=report,
                               pdf_file='example.pdf')

        # disabled for this company
        company.send_shareholder_statement_via_letter_enabled = False
        company.save()
        self.assertFalse(send_statement_letter(statement.pk))

        # no postal address
        self.assertFalse(send_statement_letter(statement.pk))

        # add postal address
        self.assertFalse(statement.user.userprofile.has_address)
        self.add_address(statement.user.userprofile)
        self.assertTrue(statement.user.userprofile.has_address)

        company.send_shareholder_statement_via_letter_enabled = True
        company.save()
        send_statement_letter(statement.pk)
        mock_upload_document.assert_called_once()

        statement.refresh_from_db()
        self.assertIsNotNone(statement.letter_sent_at)

    @override_settings(SHAREHOLDER_STATMENT_LETTER_OFFSET_DAYS=0)
    @mock.patch('shareholder.tasks.send_statement_letter.delay')
    def test_send_statement_letters(self, mock_send_statement_letter):
        send_statement_letters()
        mock_send_statement_letter.assert_not_called()

        # add shareholder statements & report
        company = CompanyGenerator().generate()
        report = mommy.make(ShareholderStatementReport, company=company,
                            report_date=now().date())

        statements = mommy.make(ShareholderStatement, report=report,
                                pdf_file='example.pdf', _quantity=2)

        # no postal address
        send_statement_letters()
        mock_send_statement_letter.assert_not_called()

        # add postal address for one user
        user_profile = statements[0].user.userprofile
        self.assertFalse(user_profile.has_address)

        self.add_address(user_profile)

        self.assertTrue(user_profile.has_address)

        send_statement_letters()

        mock_send_statement_letter.assert_called_once()

    def test_update_order_cache_task(self):
        """ update shareholder objs order_cache field """
        shareholder = ShareholderGenerator().generate()
        update_order_cache_task(shareholder.pk)
        shareholder.refresh_from_db()
        self.assertEqual(
            shareholder.order_cache,
            {u'cumulated_face_capital': 0, u'postal_code': u'12345',
             u'share_count': 0})
