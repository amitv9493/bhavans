# Generated by Django 4.2.5 on 2023-09-07 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0043_payment_receipt'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
