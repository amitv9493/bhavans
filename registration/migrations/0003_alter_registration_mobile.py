# Generated by Django 4.2.3 on 2023-07-18 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_alter_registration_members_attending_event_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='mobile',
            field=models.CharField(max_length=10),
        ),
    ]
