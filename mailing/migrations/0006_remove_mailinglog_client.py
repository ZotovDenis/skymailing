# Generated by Django 4.2.4 on 2023-09-25 17:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0005_mailinglog_response'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailinglog',
            name='client',
        ),
    ]
