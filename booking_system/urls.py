from django.urls import path
from . import views

urlpatterns = [
    path('', views.drivers_list, name='drivers_list')
]
