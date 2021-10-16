from .test_setup import TestSetUp
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import Account

class TestViews(TestSetUp):

    def test_user_can_not_register_without_data(self):
        res = self.client.post(self.register_url)

        self.assertEqual(res.status_code, 400)


    def test_user_can_register_with_data(self):
        res = self.client.post(self.register_url, self.user_register_data, format='json')
        self.assertEqual(res.status_code, 201)

    def test_user_can_not_register_with_same_data(self):
        self.client.post(self.register_url, self.user_register_data, format='json')
        res = self.client.post(self.register_url, self.user_register_data, format='json')
        self.assertEqual(res.status_code, 400)


    def test_user_can_not_login_with_unverified_email(self):
        self.client.post(self.register_url, self.user_register_data, format='json')
        res = self.client.post(self.login_url, self.user_login_data, format='json')
        self.assertEqual(res.status_code, 401)


    def test_user_can_login_with_verified_email(self):
        self.client.post(self.register_url, self.user_register_data, format='json')

        email = self.user_register_data.get('email')
        
        user = Account.objects.get(email=email)

        verification_token = RefreshToken.for_user(user).access_token

        token_data = {
            'token': str(verification_token)
        }

        self.client.post(self.verify_email_url, token_data, format='json')

        res = self.client.post(self.login_url, self.user_login_data, format='json')
        self.assertEqual(res.status_code, 200)

    def test_user_login_incorrect_email(self):
        res = self.client.post(self.login_url, self.user_login_data_false, format='json')
        self.assertEqual(res.status_code, 401)
