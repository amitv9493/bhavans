# Generated by Django 4.2.3 on 2023-07-26 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0022_alter_guest_registration_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razorpay_id', models.CharField(max_length=100)),
                ('payment_success', models.BooleanField()),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='registration.event')),
                ('registration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.registration')),
            ],
        ),
    ]
