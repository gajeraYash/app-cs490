# Generated by Django 3.1.2 on 2020-10-28 17:02

import app.models
import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_auto_20201027_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userannoucement',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, verbose_name='user_files'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pic',
            field=cloudinary.models.CloudinaryField(default=app.models.random_img, max_length=255, verbose_name='profile_pics'),
        ),
    ]