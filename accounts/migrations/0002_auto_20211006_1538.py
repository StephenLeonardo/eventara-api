# Generated by Django 3.1.3 on 2021-10-06 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='is_email_verified',
        ),
        migrations.AlterField(
            model_name='account',
            name='email',
            field=models.EmailField(error_messages={'unique': 'Account with this email already exists.'}, max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='username',
            field=models.CharField(error_messages={'unique': 'Account with this username already exists.'}, max_length=100, unique=True),
        ),
    ]