# Generated by Django 2.1.3 on 2018-11-27 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='end_time',
            field=models.TimeField(default="00:00:00"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='start_time',
            field=models.TimeField(default="00:00:00"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(),
        ),
    ]