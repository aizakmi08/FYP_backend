# Generated by Django 5.0.4 on 2024-05-02 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservationApp', '0016_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='triprequest',
            name='fare',
            field=models.FloatField(null=True),
        ),
    ]
