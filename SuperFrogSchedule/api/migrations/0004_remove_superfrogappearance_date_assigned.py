# Generated by Django 2.1.3 on 2019-02-17 04:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20190217_0403'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='superfrogappearance',
            name='date_assigned',
        ),
    ]
