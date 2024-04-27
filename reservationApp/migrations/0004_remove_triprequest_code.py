from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservationApp', '0003_alter_triprequest_date_created_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='triprequest',
            name='code',
        ),
    ]
