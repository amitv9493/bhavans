# Generated by Django 4.2.3 on 2023-07-26 14:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0021_guest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guest',
            name='registration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guest', to='registration.registration'),
        ),
        migrations.AlterField(
            model_name='registration',
            name='payment_amount',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]