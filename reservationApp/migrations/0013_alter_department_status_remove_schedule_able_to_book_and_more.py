# Generated by Django 5.0.4 on 2024-05-01 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservationApp', '0012_remove_schedule_able_to_book_schedule_able_to_book'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='status',
            field=models.CharField(choices=[('Student', 'Student'), ('Staff', 'Staff'), ('Faculty', 'Faculty')], max_length=10),
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='able_to_book',
        ),
        migrations.AddField(
            model_name='schedule',
            name='able_to_book',
            field=models.CharField(choices=[('Student', 'Student'), ('Staff', 'Staff'), ('Faculty', 'Faculty')], default='Student', max_length=10),
        ),
    ]
