from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Driver, Trip, TripUser
from .serializers import DriverSerializer, TripSerializer, TripUserSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes


# Create your views here.
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def drivers_list(request):
    if request.method == 'GET':
        drivers = Driver.objects.all()
        serializer = DriverSerializer(drivers, many=True)
        return JsonResponse({'data': serializer.data})

    if request.method == 'POST':
        serializer = DriverSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
