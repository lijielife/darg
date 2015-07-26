from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from rest_framework.test import APIClient

from shareholder.generators import UserGenerator, CompanyGenerator, ShareholderGenerator, PositionGenerator


def _add_company_to_user_via_rest(user):

    client = APIClient()
    response = client.post(
        '/services/rest/api-token-auth/',
        {'username': user.username, 'password': 'test'},
        format='json'
    )
    token = user.auth_token

    response = client.post(
        reverse('add_company'), {
            'name': 'company',
            'count': 1,
            'face_value': 2
        },
        **{
            'HTTP_AUTHORIZATION': 'Token {}'.format(token.key),
            'format': 'json',
        }
    )

    if response.status_code in [200, 201]:
        return True

    return False


class IndexTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_index_content(self):

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertTrue("social_links" in response.content)
        self.assertTrue("twitter" in response.content)
        self.assertTrue("bootstrap.min.js" in response.content)
        self.assertTrue("xeditable.min.js" in response.content)
        self.assertTrue("xeditable.css" in response.content)
        self.assertTrue("last css in" in response.content)


class TrackingTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_tracking_for_debug_mode(self):

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertTrue("UA-58468401-4" in response.content)

    def test_start_authorized(self):

        user = UserGenerator().generate()

        is_loggedin = self.client.login(username=user.username, password='test')

        self.assertTrue(is_loggedin)

        response = self.client.get(reverse('start'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("UA-58468401-4" in response.content)      # tracking code here
        self.assertTrue("Willkommen" in response.content)         # has welcome
        self.assertFalse("shareholder_list" in response.content)  # but has not shareholder list yet
        # self.assertTrue('download/pdf' in response.content)
        # self.assertTrue('download/csv' in response.content)

    def test_start_authorized_with_operator(self):

        user = UserGenerator().generate()

        is_operator_added = _add_company_to_user_via_rest(user)
        self.assertTrue(is_operator_added)

        is_loggedin = self.client.login(username=user.username, password='test')

        self.assertTrue(is_loggedin)

        response = self.client.get(reverse('start'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("UA-58468401-4" in response.content)  # tracking code here
        self.assertTrue("Willkommen" in response.content)  # has welcome
        self.assertTrue("shareholder_list" in response.content)  # has shareholder list yet, but not shown by angular

    def test_start_nonauthorized(self):

        user = UserGenerator().generate()

        is_loggedin = self.client.login(username=user.username, password='invalid_pw')

        self.assertFalse(is_loggedin)

        response = self.client.get(reverse('start'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('Login' in response.content)  # redirect to login


class DownloadTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_csv_download(self):
        """ rest download of captable csv """

        # data
        company = CompanyGenerator().generate()
        shareholder_list = []
        for x in range(1, 6):  # don't statt with 0, Generators 'if' will fail
            shareholder_list.append(ShareholderGenerator().generate(company=company, number=str(x)))

        # initial share creation
        PositionGenerator().generate(buyer=shareholder_list[0], count=1000, value=10)
        # single transaction
        PositionGenerator().generate(buyer=shareholder_list[1], count=10, value=10, seller=shareholder_list[0])
        # shareholder bought and sold
        PositionGenerator().generate(buyer=shareholder_list[2], count=20, value=20, seller=shareholder_list[0])
        PositionGenerator().generate(buyer=shareholder_list[0], count=20, value=20, seller=shareholder_list[2])

        # run test
        response = self.client.get(reverse('captable_csv', kwargs={"company_id": company.id}))

        # not logged in user
        self.assertEqual(response.status_code, 302)

        # login and retest
        user = UserGenerator().generate()
        is_loggedin = self.client.login(username=user.username, password='test')
        self.assertTrue(is_loggedin)
        response = self.client.get(reverse('captable_csv', kwargs={"company_id": company.id}))

        # assert response code
        self.assertEqual(response.status_code, 200)
        # assert proper csv
        lines = response.content.split('\r\n')
        lines.pop()  # remove last element based on final '\r\n'
        for row in lines:
            self.assertEqual(row.count(','), 5)
        self.assertEqual(len(lines), 3)  # ensure we have the right amount of data
        # assert company itself
        self.assertEqual(shareholder_list[0].number, lines[1].split(',')[0])
        # assert share owner
        self.assertEqual(shareholder_list[1].number, lines[2].split(',')[0])
        # assert shareholder witout position not in there
        for line in lines:
            self.assertNotEqual(line[0], shareholder_list[3].number)
        # assert shareholder which bought and sold again
        for line in lines:
            self.assertNotEqual(line[0], shareholder_list[2].number)

    def test_pdf_download(self):
        pass