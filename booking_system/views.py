from django.http import JsonResponse
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Driver, Trip, TripUser
from .serializers import DriverSerializer, TripSerializer, TripUserSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes


# Create your views here.
class DriversListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        drivers = Driver.objects.all()
        serializer = DriverSerializer(drivers, many=True)
        return Response({'data': serializer.data})

    def post(self, request, format=None):
        serializer = DriverSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TripListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        trips = Trip.objects.all()
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TripSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TripUserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        trip_users = TripUser.objects.all()
        serializer = TripUserSerializer(trip_users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TripUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
