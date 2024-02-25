from rest_framework import status
from rest_framework.test import APITestCase

from trader_types.models import TraderTypes
from users.models import User


class ProductTestCase(APITestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create(email='user1@email.com', password='123')
        self.trader_types = ['Завод', 'Розничная сеть', 'Индивидуальный предприниматель']

    def test_exist_trader_types(self):
        # Case 1: Типы звеньев существуют
        db_trader_types = TraderTypes.objects.all()
        self.assertEqual(len(db_trader_types), 3)

        # Case 2: Типы звеньев из списка
        [self.assertTrue(db_type.title in self.trader_types) for db_type in db_trader_types]
