# Generated by Django 4.2.3 on 2023-07-24 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0018_remove_event_amount_event_is_this_main'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='amount',
            field=models.PositiveIntegerField(default=100),
        ),
    ]
