from rest_framework import status
from rest_framework.test import APITestCase

from products.models import Product
from traders.models import Trader
from users.models import User


class ProductTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email='user@email.com', password='123')
        self.data_trader1 = {
            "title": "Продавец 1",
        }
        self.data_trader2 = {
            "title": "Продавец 2",
        }
        self.data_trader3 = {
            "title": "Продавец 3",
        }

        self.data_trader4 = {
            "title": "Продавец 4",
        }

        self.data_trader5 = {
            "title": "Продавец 5",
        }

    def test_create_traders(self):
        # Case 1: Создание продавца неавторизованным пользователем
        response = self.client.post('/traders/', data=self.data_trader1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Case 2: Создание продавца авторизованным пользователем
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/traders/', data=self.data_trader1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json().get('title'), self.data_trader1['title'])

        # Case 3: Создание цепочки продавцов длиннее 3 звеньев
        self.data_trader2['vendor'] = response.json().get('id')
        response = self.client.post('/traders/', data=self.data_trader2)
        self.data_trader3['vendor'] = response.json().get('id')
        response = self.client.post('/traders/', data=self.data_trader3)
        self.data_trader4['vendor'] = response.json().get('id')
        response = self.client.post('/traders/', data=self.data_trader4)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Case 4: Создание продавца c дублем названия
        response = self.client.post('/traders/', data={
            'title': self.data_trader1['title']
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_traders(self):
        trader1 = Trader.objects.create(**self.data_trader1)

        # Case 1: Получение списка продавцов неавторизованным пользователем
        response = self.client.get('/traders/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Case 2: Получение списка продавцов авторизованным пользователем
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/traders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['title'], trader1.title)

    def test_retrieve_traders(self):
        trader1 = Trader.objects.create(**self.data_trader1)

        # Case 1: Просмотр продавца неавторизованным пользователем
        response = self.client.get(f'/traders/{trader1.pk}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Case 2: Просмотр продавца авторизованным пользователем
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/traders/{trader1.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('title'), trader1.title)

    def test_update_traders(self):
        trader1 = Trader.objects.create(**self.data_trader1)
        self.data_trader2['vendor'] = trader1
        trader2 = Trader.objects.create(**self.data_trader2)
        self.data_trader3['vendor'] = trader2
        trader3 = Trader.objects.create(**self.data_trader3)
        trader4 = Trader.objects.create(**self.data_trader4)

        # Case 1: Обновление продавца неавторизованным пользователем
        response = self.client.put(f'/traders/{trader4.pk}/', data=self.data_trader5)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Case 2: Обновление продавца авторизованным пользователем
        self.client.force_authenticate(user=self.user)
        response = self.client.put(f'/traders/{trader4.pk}/', data=self.data_trader5)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('title'), self.data_trader5['title'])

        # Case 3: Обновление задолженности
        self.data_trader5['debt'] = 55.2
        response = self.client.put(f'/traders/{trader4.pk}/', self.data_trader5)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.json().get('debt'))

        # Case 4: Обновление поставщика, поставщик 0-го уровня
        self.data_trader5['vendor'] = trader1.pk
        response = self.client.put(f'/traders/{trader4.pk}/', self.data_trader5)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('vendor'), trader1.pk)

        # Case 5: Обновление поставщика, поставщик уже 2-го уровня
        self.data_trader5['vendor'] = trader3.pk
        response = self.client.put(f'/traders/{trader4.pk}/', self.data_trader5)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Case 5: Обновление поставщика, дочерние элементы станут выше 2 уровня
        self.data_trader1['vendor'] = trader4.pk
        response = self.client.put(f'/traders/{trader1.pk}/', self.data_trader1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_traders(self):
        trader = Trader.objects.create(**self.data_trader1)

        # Case 1: Удаление продавца неавторизованным пользователем
        response = self.client.delete(f'/traders/{trader.pk}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Case 2: Удаление продавца авторизованным пользователем
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/traders/{trader.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Trader.objects.filter(title=self.data_trader1['title']).exists())
