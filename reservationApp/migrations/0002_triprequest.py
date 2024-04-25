# Generated by Django 4.0.3 on 2024-04-25 15:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reservationApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TripRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('schedule', models.DateTimeField()),
                ('fare', models.FloatField()),
                ('status', models.CharField(choices=[('1', 'Active'), ('2', 'Cancelled')], default=1, max_length=2)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservationApp.bus')),
                ('depart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_depart_location', to='reservationApp.location')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_destination', to='reservationApp.location')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
