# Generated by Django 3.1.3 on 2020-12-01 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user_location',
        ),
        migrations.DeleteModel(
            name='HoldModel',
        ),
    ]