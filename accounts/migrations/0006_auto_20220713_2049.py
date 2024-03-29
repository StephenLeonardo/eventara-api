# Generated by Django 3.1.3 on 2022-07-13 13:49

import accounts.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizers', '0002_organizer_abbreviation'),
        ('accounts', '0005_auto_20211212_2154'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='organizers.organizer'),
        ),
        migrations.AlterField(
            model_name='account',
            name='profile_picture',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to=accounts.models.path_and_rename, validators=[accounts.models.Account.validate_image]),
        ),
    ]
