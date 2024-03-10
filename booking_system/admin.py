from django.contrib import admin
from .models import Trip, TripUser, Driver

# Register your models here.
admin.site.register(Trip)
admin.site.register(TripUser)
admin.site.register(Driver)