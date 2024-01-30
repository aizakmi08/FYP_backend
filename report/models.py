from django.db import models
from booking_system.models import Booking

# Create your models here.


class Report(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    fuel_spent = models.DecimalField(max_digits=6, decimal_places=2)  # in liters
    kilometers = models.DecimalField(max_digits=8, decimal_places=2)  # in kilometers
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.booking.user.username} - {self.booking.trip.destination}"