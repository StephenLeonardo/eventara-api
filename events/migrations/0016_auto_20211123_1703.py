# Generated by Django 3.1.3 on 2021-11-23 10:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_auto_20211111_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='eventimage',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='events.event'),
        ),
        migrations.AlterField(
            model_name='eventimage',
            name='image',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
    ]
