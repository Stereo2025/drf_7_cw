import django
django.setup()
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from users.models import User


class UserTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        User.objects.all().delete()

    def test_register_success(self):
        data = {
            'email': 'testr@example.com',
            'password': '324q1@r1334A',
            'telegram_id': '0'
        }

        response = self.client.post(
            reverse('users:register'),
            data=data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.json()
        self.assertIn('id', response_data)
        self.assertEqual(response_data['email'], data['email'])

    def test_register_missing_password(self):
        data = {
            'email': 'testr@example.com',
            'telegram_id': '0'
        }

        response = self.client.post(
            reverse('users:register'),
            data=data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertIn('password', response.json())


    def test_register_invalid_email(self):
        data = {
            'email': 'invalid-email',
            'password': '324q1@r1334A',
            'telegram_id': '0'
        }

        response = self.client.post(
            reverse('users:register'),
            data=data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertIn('email', response.json())

    def test_register_existing_email(self):
        existing_user_data = {
            'email': 'existing@example.com',
            'password': 'ExistingPass123@',
            'telegram_id': '1'
        }
        self.client.post(
            reverse('users:register'),
            data=existing_user_data,
            format='json'
        )

        new_user_data = {
            'email': 'existing@example.com',
            'password': 'NewPass456@',
            'telegram_id': '2'
        }
        response = self.client.post(
            reverse('users:register'),
            data=new_user_data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertIn('email', response.json())
