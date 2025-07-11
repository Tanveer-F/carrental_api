from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User

class UserAuthTests(APITestCase):

# user registration tests:
    def test_user_registration(self):
        url = reverse('register')
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "strongpass123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())

# user login tests:
    def test_user_login(self):
        User.objects.create_user(username="loginuser", password="loginpass123")
        url = reverse('token_obtain_pair')
        data = {
            "username": "loginuser",
            "password": "loginpass123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_registration_missing_password(self):
        url = reverse('register')
        data = {
            "username": "nopassuser",
            "email": "no@pass.com"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_registration_duplicate_username(self):
        User.objects.create_user(username="duplicate", password="somepass")
        url = reverse('register')
        data = {
            "username": "duplicate",
            "email": "dup@example.com",
            "password": "anotherpass"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)

    def test_login_with_wrong_password(self):
        User.objects.create_user(username="wrongpassuser", password="correctpass")
        url = reverse('token_obtain_pair')
        data = {
            "username": "wrongpassuser",
            "password": "wrongpass"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
