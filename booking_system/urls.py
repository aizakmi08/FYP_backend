from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from .views import DriversListView, TripListView, TripUserView

urlpatterns = [
    path('drivers/', DriversListView.as_view(), name='drivers_list'),
    path('trips/', TripListView.as_view(), name='trips_list'),
    path('trip_user/', TripUserView.as_view(), name='trip_users_list'),
]
