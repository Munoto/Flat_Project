# Generated by Django 5.0.4 on 2024-05-24 13:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0012_remove_apartment_image_image_apartment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='about',
            name='apartment',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='about', to='backend.apartment'),
        ),
    ]
