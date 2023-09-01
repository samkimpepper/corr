import json 
from django.test import TestCase
from django.urls import reverse 
from .models import Account 
from rest_framework.test import APITestCase 
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken

# Create your tests here.
class RegisterTestCase(APITestCase):
    url = reverse("account:register")

    def test_registration(self):
        req_data = {
            "username": "testuser",
            "email": "test@gmail.com",
            "password": "password",
            "check_password": "invalid_password"
        }
        res = self.client.post(self.url, req_data)
        self.assertEqual(201, res.status_code)

    def test_unique_email_validation(self):
        req_data_1 = {
            "username": "testuser",
            "email": "test@gmail.com",
            "password": "password"
        }
        res = self.client.post(self.url, req_data_1)
        self.assertEqual(201, res.status_code)

        req_data_2 = {
            "username": "testuser",
            "email": "test@gmail.com",
            "password": "password"
        }
        res = self.client.post(self.url, req_data_2)
        self.assertEqual(400, res.status_code)

class LoginAPIViewTestCase(APITestCase):
    url = reverse("account:login")

    def setUp(self):
        self.username = "duck"
        self.email = "duck@gmail.com"
        self.password = "duckduck"
        self.user = Account.objects.create_user(self.username, self.email, self.password)

    def test_authentication_with_wrong_password(self):
        res = self.client.post(self.url, {"username": self.username, "password": "invalid_password"})
        self.assertEqual(400, res.status_code)

    def test_authentication_with_valid_data(self):
        res = self.client.post(self.url, {"username": self.username, "password": self.password})
        self.assertEqual(200, res.status_code)
        self.assertTrue("access_token" in json.loads(res.content))

class LogoutAPIViewTestCase(APITestCase):
    url = reverse('account:logout')

    def setUp(self):
        self.user = Account.objects.create_user(username='testuser', password='testpassword')
        self.token = RefreshToken.for_user(self.user)
        self.refresh_token = str(self.token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')

    def test_logout_success(self):
        res = self.client.post(self.url, {'refresh_token': self.refresh_token})
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, Token.objects.count())


