# Generated by Django 4.2.4 on 2023-09-24 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0004_alter_mailingsettings_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailinglog',
            name='response',
            field=models.CharField(default='None', max_length=200, verbose_name='Ответ сервера'),
        ),
    ]
