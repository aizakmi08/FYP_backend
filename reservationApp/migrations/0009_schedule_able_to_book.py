# Generated by Django 5.0.4 on 2024-05-01 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservationApp', '0008_rename_profile_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='able_to_book',
            field=models.ManyToManyField(related_name='bookable_trips', to='reservationApp.department'),
        ),
    ]
