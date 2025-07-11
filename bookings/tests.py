from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from vehicles.models import Vehicle
from bookings.models import Booking

class BookingAPITests(APITestCase):

    def setUp(self):
        # Create and authenticate a user
        self.user = User.objects.create_user(username='booker', password='bookpass123')
        self.client.login(username='booker', password='bookpass123')

        # Get JWT token
        response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'booker',
            'password': 'bookpass123'
        })
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        # Create a vehicle for booking
        self.vehicle = Vehicle.objects.create(
            owner=self.user,
            make="Toyota",
            model="Yaris",
            year=2022,
            plate="BOOK-123"
        )

    def test_create_booking(self):
        url = '/api/bookings/'
        data = {
            "vehicle": self.vehicle.id,
            "start_date": "2025-07-15",
            "end_date": "2025-07-20"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)

    def test_list_user_bookings(self):
        Booking.objects.create(user=self.user, vehicle=self.vehicle,
                               start_date="2025-07-10", end_date="2025-07-12")
        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_user_cannot_book_vehicle_with_invalid_dates(self):
        url = '/api/bookings/'
        data = {
            "vehicle": self.vehicle.id,
            "start_date": "2025-07-25",
            "end_date": "2025-07-20"  # end date before start
        }
        response = self.client.post(url, data, format='json')
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])

    def test_user_cannot_see_others_bookings(self):
        other_user = User.objects.create_user(username='outsider', password='test123')
        Booking.objects.create(user=other_user, vehicle=self.vehicle,
                               start_date="2025-08-01", end_date="2025-08-05")

        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # Should not see others' bookings

    def test_booking_is_linked_to_logged_in_user(self):
        url = '/api/bookings/'
        data = {
            "vehicle": self.vehicle.id,
            "start_date": "2025-09-01",
            "end_date": "2025-09-05"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        booking = Booking.objects.first()
        self.assertEqual(booking.user, self.user)

    def test_prevent_overlapping_bookings(self):
        # First booking
        Booking.objects.create(
            user=self.user,
            vehicle=self.vehicle,
            start_date="2025-08-01",
            end_date="2025-08-05"
        )

        # Attempt overlapping booking
        data = {
            "vehicle": self.vehicle.id,
            "start_date": "2025-08-03",  # overlaps with above
            "end_date": "2025-08-07"
        }
        response = self.client.post('/api/bookings/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("already booked", str(response.data))