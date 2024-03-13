from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from .views import DriversListView

urlpatterns = [
    path('drivers/', DriversListView.as_view(), name='drivers_list')


]
