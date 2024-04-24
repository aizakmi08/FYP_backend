from rest_framework import serializers
from .models import Driver, Trip, TripUser


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'


class TripSerializer(serializers.ModelSerializer):
    driver = serializers.SlugRelatedField(slug_field='name', queryset=Driver.objects.all(), allow_null=True)

    class Meta:
        model = Trip
        fields = '__all__'


class TripUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripUser
        fields = '__all__'
