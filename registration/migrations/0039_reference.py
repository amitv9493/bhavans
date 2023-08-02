# Generated by Django 4.2.3 on 2023-08-02 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0038_alter_registration_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('registration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.registration', verbose_name='Reffered By')),
            ],
        ),
    ]
