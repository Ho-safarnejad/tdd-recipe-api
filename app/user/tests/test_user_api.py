from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


USER_CREATE_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """ Test user api publicly without auhtentication """

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_seccessful(self):
        """ Test create user with valid payload. """
        payload = {
            'email': 'test@borna.com',
            'password': 'testpass',
            'name': 'test full name'
        }
        res = self.client.post(USER_CREATE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exist(self):
        """ Test failure in creating a user that already exist. """
        payload = {
            'email': 'test@borna.com',
            'password': 'testpass'
        }
        create_user(**payload)
        res = self.client.post(USER_CREATE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_to_short(self):
        """ Tests failure iin creating a user with short password. """
        payload = {
            'email': 'test@borna.com',
            'password': 'pw'
        }
        res = self.client.post(USER_CREATE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """ Test a token is created for a user """
        payload = {
            'email': 'test@borna.com',
            'password': 'testpass',
            'name': 'test full name'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_invalid_credential_to_get_token(self):
        """ Test if the credentials are not correct to get a token"""
        create_user(email='test@borna.com', password='testpass')
        payload = {
            'email': 'test@borna.com',
            'password': 'wrongpass'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_with_no_user(self):
        """ Test tooken does not generate if user is not created"""
        payload = {
            'email': 'test@borna.com',
            'password': 'wrongpass'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_with_missing_fields(self):
        """ Test get token with missing fields """
        res = self.client.post(TOKEN_URL, {'email': 'test', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
