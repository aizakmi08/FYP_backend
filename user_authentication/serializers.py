from rest_framework import serializers
from .models import User, Department


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Department.objects.all(),
        source='department'
    )

    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'surname', 'phone_number', 'department', 'department_id', 'is_admin')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
