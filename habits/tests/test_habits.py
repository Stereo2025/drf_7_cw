import django
django.setup()
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from habits.models import Habit
from rest_framework.exceptions import ErrorDetail
from django.utils.timezone import make_aware
from datetime import datetime


class HabitTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'testr@example.com',
            'password': '324q1@r1334A',
            'telegram_id': '0'
        }
        self.register_url = reverse('users:register')
        self.user = User.objects.create_user(**self.user_data)
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        self.public_habit = Habit.objects.create(
            author=self.user,
            place='Park',
            time=make_aware(datetime(2023, 1, 1, 10, 0, 0)),
            action='Running',
            pleasant=True,
            periodicity=2,
            reward='Ice Cream',
            complete_time=make_aware(datetime(2023, 1, 1, 10, 30, 0)),
            is_public=True
        )
        self.private_habit = Habit.objects.create(
            author=self.user,
            place='Home',
            time=make_aware(datetime(2023, 1, 2, 10, 0, 0)),
            action='Reading',
            pleasant=False,
            periodicity=3,
            reward='Candy',
            complete_time=make_aware(datetime(2023, 1, 2, 11, 0, 0)),
            is_public=False
        )

    def test_register_success(self):

        response = self.client.post(
            self.register_url,
            data=self.user_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['email'],
            [ErrorDetail(string='пользователь с таким Почта уже существует.', code='unique')]
        )

    def test_create_habit(self):
        url = reverse('habits:habit-create')
        data = {
            'author': self.user.id,
            'place': 'Home',
            'time': '08:00:00',
            'action': 'Exercise',
            'pleasant': True,
            'complete_time': '2023-10-10T08:30:00Z',
            'periodicity': 1,
            'is_public': True,
        }

        try:
            response = self.client.post(url, data, format='json')
            print(response.data)
        except Exception as e:
            print(f"Exception: {e}")
            raise e

        if response.status_code != status.HTTP_201_CREATED:
            print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 3)
        self.assertEqual(Habit.objects.get(id=response.data['id']).action, 'Exercise')

    def test_get_public_habits(self):
        url = reverse('habits:public-habit-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['action'], 'Running')

    def test_get_user_habits(self):
        url = reverse('habits:owner-habit-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_get_habit_detail(self):
        url = reverse('habits:habit-detail', args=[self.public_habit.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['place'], 'Park')

    def test_update_habit(self):
        url = reverse('habits:habit-detail', args=[self.public_habit.id])
        data = {
            'author': self.user.id,
            'place': 'Park',
            'time': '08:00:00',
            'action': 'Updated Habit',
            'pleasant': False,
            'complete_time': '2023-10-10T08:30:00Z',
            'periodicity': 2,
            'is_public': True,
        }
        response = self.client.put(url, data, format='json')
        if response.status_code != status.HTTP_200_OK:
            print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_habit = Habit.objects.get(id=self.public_habit.id)
        self.assertEqual(updated_habit.place, 'Park')
        self.assertEqual(updated_habit.action, 'Updated Habit')

    def test_delete_habit(self):
        url = reverse('habits:habit-detail', args=[self.public_habit.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 1)

    def test_filter_public_habits(self):
        url = reverse('habits:public-habit-list') + '?sign_of_pleasant=true'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1, f"Expected 4 items, but got {len(response.data['results'])}")
        if len(response.data['results']) > 0:
            self.assertEqual(response.data['results'][0]['place'], 'Park')
        else:
            self.fail("Response data is empty. Expected at least one item.")