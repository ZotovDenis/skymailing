# Generated by Django 4.2.4 on 2023-09-19 20:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': [('set_active', 'Can change user activity')]},
        ),
    ]
