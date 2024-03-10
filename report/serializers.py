from rest_framework import serializers
from .models import Report, Department

class ReportSerializer(serializers.ModelSerializer):
    department = serializers.SlugRelatedField(slug_field='name', queryset=Department.objects.all())
    class Meta:
        model = Report
        fields = '__all__'
