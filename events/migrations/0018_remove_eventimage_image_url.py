# Generated by Django 3.1.3 on 2021-12-09 05:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0017_auto_20211123_1703'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventimage',
            name='image_url',
        ),
    ]
