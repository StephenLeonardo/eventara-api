# Generated by Django 3.1.3 on 2021-11-11 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_auto_20211111_1354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to='events/11-2021/'),
        ),
    ]