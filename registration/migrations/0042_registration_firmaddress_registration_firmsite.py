# Generated by Django 4.2.3 on 2023-08-08 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0041_registration_image_alter_reference_has_joined'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='firmAddress',
            field=models.TextField(blank=True, null=True, verbose_name='Firm Name'),
        ),
        migrations.AddField(
            model_name='registration',
            name='firmSite',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Firm Site'),
        ),
    ]
