# Generated by Django 5.0.4 on 2024-05-16 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_remove_about_apartment_apartment_about'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='phone_number',
            field=models.IntegerField(default=87472740019),
            preserve_default=False,
        ),
    ]
