from rest_framework import serializers
from .models import Booking
from django.db.models import Q

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'vehicle', 'start_date', 'end_date']

    def validate(self, data):
        vehicle = data.get('vehicle')
        start = data.get('start_date')
        end = data.get('end_date')

        if start >= end:
            raise serializers.ValidationError("End date must be after start date.")

        # Check for overlapping bookings for the same vehicle
        overlapping = Booking.objects.filter(
            vehicle=vehicle,
            start_date__lt=end,
            end_date__gt=start
        )

        if overlapping.exists():
            raise serializers.ValidationError("This car is already booked for the selected dates.")

        return data