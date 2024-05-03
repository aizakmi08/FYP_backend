from django.contrib import admin
from reservationApp.models import Category, Department, Location, Bus, Schedule, Booking, TripRequest, Driver
# Register your models here.
admin.site.register(Department)
admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Bus)
admin.site.register(Schedule)
admin.site.register(Booking)
admin.site.register(TripRequest)
admin.site.register(Driver)
