# Generated by Django 3.1.3 on 2020-12-08 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_userprofile_user_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_bio',
            field=models.TextField(blank=True, max_length=256),
        ),
    ]
