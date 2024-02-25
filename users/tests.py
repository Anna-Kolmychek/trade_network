from django.core.management import call_command
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class ProductTestCase(APITestCase):
    def setUp(self) -> None:
        call_command('create_su')
        self.admin = User.objects.filter(email='admin@email.com').first()
        self.user = User.objects.create(email='user@email.com', password='123')
        self.data_user1 = {
            'email': 'user1@email.com',
            'password': '123'
        }
        self.data_user2 = {
            'email': 'user2@email.com',
            'password': '123'
        }

    def test_create_users(self):
        # Case 1: Создание пользователя неавторизованным пользователем
        response = self.client.post('/users/', data=self.data_user1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Case 2: Создание пользователя неавторизованным пользователем
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/users/', data=self.data_user1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Case 3: Создание пользователя админом
        self.client.force_authenticate(user=self.admin)
        response = self.client.post('/users/', data=self.data_user1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json().get('email'), self.data_user1['email'])

        # Case 4: Создание пользователя c дублем почты
        response = self.client.post('/users/', data={
            'title': self.data_user1['email']
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_users(self):
        db_user1 = User.objects.create(**self.data_user1)

        # Case 1: Получение списка пользователей неавторизованным пользователем
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Case 2: Получение списка пользователей не админом
        response = self.client.get('/users/')
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Case 3: Получение списка пользователей авторизованным пользователем
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 3)

    def test_retrieve_users(self):
        db_user1 = User.objects.create(**self.data_user1)

        # Case 1: Просмотр пользователя неавторизованным пользователем
        response = self.client.get(f'/users/{db_user1.pk}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Case 2: Просмотр пользователя не админом
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/users/{db_user1.pk}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Case 3: Просмотр пользователя авторизованным пользователем
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(f'/users/{db_user1.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('email'), self.data_user1['email'])

    def test_update_users(self):
        db_user1 = User.objects.create(**self.data_user1)

        # Case 1: Обновление пользователя неавторизованным пользователем
        response = self.client.put(f'/users/{db_user1.pk}/', data=self.data_user2)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Case 2: Обновление пользователя не админом
        self.client.force_authenticate(user=self.user)
        response = self.client.put(f'/users/{db_user1.pk}/', data=self.data_user2)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Case 3: Обновление пользователя админом
        self.client.force_authenticate(user=self.admin)
        response = self.client.put(f'/users/{db_user1.pk}/', data=self.data_user2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('email'), self.data_user2['email'])

    def test_delete_users(self):
        db_user1 = User.objects.create(**self.data_user1)

        # Case 1: Удаление пользователя неавторизованным пользователем
        response = self.client.delete(f'/users/{db_user1.pk}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Case 2: Удаление пользователя не админом
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/users/{db_user1.pk}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Case 3: Удаление пользователя админом
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f'/users/{db_user1.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(email=self.data_user1['email']).exists())
