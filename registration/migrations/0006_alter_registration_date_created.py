# Generated by Django 4.2.3 on 2023-07-19 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0005_registration_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
