# Generated by Django 4.2.3 on 2023-08-08 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0042_registration_firmaddress_registration_firmsite'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='receipt',
            field=models.FileField(blank=True, null=True, upload_to='media'),
        ),
    ]
