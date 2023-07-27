# Generated by Django 4.2.3 on 2023-07-27 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0028_alter_payment_payment_amt_alter_payment_payment_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='razorpay_id',
            new_name='razorpay_order_id',
        ),
        migrations.AddField(
            model_name='payment',
            name='razorpay_payment_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='razorpay_signature_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_success',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
