# Generated by Django 5.0.4 on 2024-05-14 01:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_customuser_is_active_customuser_is_staff_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='is_superuser',
        ),
    ]
