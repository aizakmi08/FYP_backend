from django.db import models
from user.models import User


# Create your models here.
class Driver(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.name} - {self.surname}"


class Trip(models.Model):
    car_type = (
        ("4", "Small Car"),
        ("28", "Bus")
    )
    title = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    pick_up_destination = models.CharField(max_length=200)
    drop_off_destination = models.CharField(max_length=200)
    car_type = models.CharField(choices=car_type, max_length=50)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)
    distance = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.title


class TripUser(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('trip', 'user',)
