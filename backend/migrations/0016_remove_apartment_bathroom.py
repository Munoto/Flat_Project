# Generated by Django 5.0.4 on 2024-05-29 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0015_apartment_latitude_apartment_longitude_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apartment',
            name='bathroom',
        ),
    ]