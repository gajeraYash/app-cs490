# Generated by Django 3.1.1 on 2020-10-03 03:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20201003_0309'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='created',
        ),
    ]