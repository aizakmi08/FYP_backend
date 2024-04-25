# Generated by Django 4.0.3 on 2024-04-25 15:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('reservationApp', '0002_triprequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='triprequest',
            name='date_created',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='triprequest',
            name='date_updated',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='triprequest',
            name='schedule',
            field=models.DateField(),
        ),
    ]
