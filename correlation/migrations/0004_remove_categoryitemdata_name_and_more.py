# Generated by Django 4.1.3 on 2022-12-20 05:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('correlation', '0003_categoryitemdata_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoryitemdata',
            name='name',
        ),
        migrations.AlterField(
            model_name='categoryitemdata',
            name='existence',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='categoryitemdata',
            name='recorded_time',
            field=models.TimeField(default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='categoryitemdata',
            name='strength',
            field=models.IntegerField(null=True),
        ),
    ]