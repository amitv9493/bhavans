# Generated by Django 4.2.3 on 2023-08-01 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0036_rename_name_registration_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='address',
            field=models.TextField(default=343434),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registration',
            name='anniversary_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='registration',
            name='city',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='registration',
            name='cityISO',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='registration',
            name='country',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='registration',
            name='countryISO',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='registration',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='registration',
            name='state',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='registration',
            name='stateISO',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]