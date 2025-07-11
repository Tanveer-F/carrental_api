from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from vehicles.models import Vehicle

class VehicleAPITests(APITestCase):

    def setUp(self):
        # Create and authenticate a user
        self.user = User.objects.create_user(username='caruser', password='carpass123')
        self.client.login(username='caruser', password='carpass123')

        # Get JWT token
        response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'caruser',
            'password': 'carpass123'
        })
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_add_vehicle(self):
        url = '/api/vehicles/'
        data = {
            "make": "Toyota",
            "model": "Corolla",
            "year": 2020,
            "plate": "ABC-123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vehicle.objects.count(), 1)

    def test_list_vehicles(self):
        Vehicle.objects.create(owner=self.user, make="Honda", model="Civic", year=2019, plate="XYZ-789")
        response = self.client.get('/api/vehicles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_vehicle(self):
        vehicle = Vehicle.objects.create(owner=self.user, make="Suzuki", model="Swift", year=2018, plate="SWF-001")
        url = f'/api/vehicles/{vehicle.id}/'
        data = {
            "make": "Suzuki",
            "model": "Alto",
            "year": 2021,
            "plate": "ALT-999"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['model'], "Alto")

    def test_delete_vehicle(self):
        vehicle = Vehicle.objects.create(owner=self.user, make="Nissan", model="Sunny", year=2017, plate="SUN-123")
        url = f'/api/vehicles/{vehicle.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vehicle.objects.count(), 0)

    def test_user_cannot_see_others_vehicles(self):
        other_user = User.objects.create_user(username='other', password='other123')
        Vehicle.objects.create(owner=other_user, make="BMW", model="X5", year=2022, plate="BMW-555")

        response = self.client.get('/api/vehicles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # Should not see other user's cars