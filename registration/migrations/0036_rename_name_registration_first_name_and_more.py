# Generated by Django 4.2.3 on 2023-08-01 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0035_alter_guest_event'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registration',
            old_name='name',
            new_name='first_name',
        ),
        migrations.AddField(
            model_name='registration',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
