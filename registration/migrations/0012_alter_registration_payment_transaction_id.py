# Generated by Django 4.2.3 on 2023-07-21 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0011_alter_registration_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='payment_transaction_id',
            field=models.CharField(default='sdsfs', max_length=100),
            preserve_default=False,
        ),
    ]