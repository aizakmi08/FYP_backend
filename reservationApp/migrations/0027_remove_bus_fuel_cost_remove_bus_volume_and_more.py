# Generated by Django 5.0.4 on 2024-05-15 20:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservationApp', '0026_bus_fuel_cost_bus_volume_schedule_distance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bus',
            name='fuel_cost',
        ),
        migrations.RemoveField(
            model_name='bus',
            name='volume',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='distance',
        ),
    ]