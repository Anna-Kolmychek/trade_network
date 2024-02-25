from rest_framework import status
from rest_framework.test import APITestCase

from products.models import Product
from users.models import User


class ProductTestCase(APITestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create(email='user1@email.com', password='123')
        self.data_product1 = {
            'title': 'Продукт 1',
            'model': 'Модель 1',
            'release_date': '2024-01-01',
        }
        self.data_product2 = {
            'title': 'Продукт 2'
        }
        self.data_product3 = {
            'title': 'Продукт 3',
            'model': 'Модель 3',
            'release_date': '2024-01-02',
        }

    def test_create_products(self):
        # Case 1: Создание продукта неавторизованным пользователем
        response = self.client.post('/products/', data=self.data_product1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Case 2: Создание продукта авторизованным пользователем
        self.client.force_authenticate(user=self.user1)
        response = self.client.post('/products/', data=self.data_product1)
        self.data_product1['id'] = response.json().get('id')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), self.data_product1)

        # Case 3: Создание продукта c дублем имени
        response = self.client.post('/products/', data={
            'title': self.data_product1['title']
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_products(self):
        product1 = Product.objects.create(**self.data_product1)
        self.data_product1['id'] = product1.pk

        # Case 1: Получение списка продуктов неавторизованным пользователем
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Case 2: Получение списка продуктов авторизованным пользователем
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [self.data_product1])

    def test_retrieve_products(self):
        product1 = Product.objects.create(**self.data_product1)
        self.data_product1['id'] = product1.pk

        # Case 1: Просмотр продукта неавторизованным пользователем
        response = self.client.get(f'/products/{product1.pk}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Case 2: Просмотр продукта авторизованным пользователем
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(f'/products/{product1.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), self.data_product1)

    def test_update_products(self):
        product = Product.objects.create(**self.data_product1)

        # Case 1: Обновление продукта неавторизованным пользователем
        response = self.client.put(f'/products/{product.pk}/', data=self.data_product3)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Case 2: Обновление продукта авторизованным пользователем. Полные данные
        self.client.force_authenticate(user=self.user1)
        response = self.client.put(f'/products/{product.pk}/', data=self.data_product3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.data_product3['id'] = product.pk
        self.assertEqual(response.json(), self.data_product3)

        # Case 3: Обновление продукта авторизованным пользователем. Частичные данные
        self.client.force_authenticate(user=self.user1)
        response = self.client.put(f'/products/{product.pk}/', data=self.data_product2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.data_product3['title'] = self.data_product2['title']
        self.assertEqual(response.json(), self.data_product3)

    def test_delete_products(self):
        product = Product.objects.create(**self.data_product1)

        # Case 1: Удаление продукта неавторизованным пользователем
        response = self.client.delete(f'/products/{product.pk}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Case 2: Удаление продукта авторизованным пользователем
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(f'/products/{product.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(title=self.data_product1['title']).exists())
