# Generated by Django 4.1.3 on 2022-12-24 06:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('correlation', '0005_rename_strength_categoryitemdata_figure_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='categoryitemdata',
            old_name='recorded_date',
            new_name='created_date',
        ),
        migrations.AddField(
            model_name='categoryitemdata',
            name='created_time',
            field=models.TimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='categoryitem',
            name='record_type',
            field=models.CharField(choices=[('유무', 'Existence'), ('강도', 'Strength'), ('시각', 'Time')], default='유무', max_length=10),
        ),
        migrations.AlterField(
            model_name='categoryitemdata',
            name='recorded_time',
            field=models.TimeField(null=True),
        ),
    ]