from django.db import models
from user.models import User
import datetime


# Create your models here.

class Car(models.Model):
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    fuel_efficiency = models.DecimalField(max_digits=5, decimal_places=2)  # liters per 100km

    def __str__(self):
        return f"{self.name} {self.model}"


class Trip(models.Model):
    destination = models.CharField(max_length=255)
    distance = models.DecimalField(max_digits=8, decimal_places=2)  # in kilometers

    def __str__(self):
        return self.destination

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)
    trip = models.ForeignKey(Trip, on_delete=models.SET_NULL, null=True)
    booking_time = models.DateTimeField(auto_now_add=True)
    trip_time = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.trip.destination}"

    def clean(self):
        # Ensure the booking is at least 1 hour in the future
        if self.trip_time < datetime.datetime.now() + datetime.timedelta(hours=1):
            raise ValueError("Booking must be at least 1 hour in advance.")
