# Generated by Django 3.1.2 on 2020-10-09 05:38

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0011_user_annoucements'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User_Annoucements',
            new_name='UserAnnoucements',
        ),
    ]
