# Generated by Django 5.0.4 on 2024-05-02 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservationApp', '0022_booking_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='triprequest',
            name='seats',
            field=models.IntegerField(null=True),
        ),
    ]