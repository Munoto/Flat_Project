from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Apartment, CustomUser


class ApartmentFilterTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Создание тестовых данных
        self.user = CustomUser.objects.create(username='testuser', password='password123')

        Apartment.objects.create(
            type='Apartment',
            rent_type='Monthly',
            name='Test Apartment 1',
            price=1500,
            description='A nice place',
            count_of_rooms='3',
            region='Central',
            street='Main St',
            house_number='1',
            longitude=50,
            latitude=50,
            year_of_construction=2000,
            max_floor=10,
            floor=5,
            height=3,
            apartment_area=100,
            kitchen_area=20,
            user=self.user
        )

        Apartment.objects.create(
            type='Studio',
            rent_type='Daily',
            name='Test Apartment 2',
            price=2000,
            description='Another nice place',
            count_of_rooms='1',
            region='Central',
            street='Second St',
            house_number='2',
            longitude=60,
            latitude=60,
            year_of_construction=2010,
            max_floor=15,
            floor=10,
            height=3,
            apartment_area=80,
            kitchen_area=15,
            user=self.user
        )

    def test_filter_apartments_by_price(self):
        response = self.client.get('/apartment/list/', {'price__gte': 1500, 'price__lte': 2000})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_apartments_by_region(self):
        response = self.client.get('/apartment/list/', {'region': 'Central'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_apartments_by_type(self):
        response = self.client.get('/apartment/list/', {'type': 'Studio'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Apartment 2')
