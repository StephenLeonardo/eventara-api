from drf_yasg.openapi import PathItem
from rest_framework.test import APITestCase
from django.urls import reverse

class TestSetUp(APITestCase):



    def setUp(self):
        self.register_url = reverse('account-list')
        self.login_url = reverse('account-login')
        self.verify_email_url = reverse('account-email-verification')

        self.user_register_data = {
            'username': 'Test Account 123',
            'email': 'user@example.com',
            'password': 'string',
            'profile_picture': None,
            'description': None
        }


        self.user_login_data = {
            'email': 'user@example.com',
            'password': 'string',
        }

        self.user_login_data_false = {
            'email': 'banned@gmail.com',
            'password': '123'
        }


        return super().setUp()

    def tearDown(self):
        return super().tearDown()