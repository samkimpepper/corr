# Generated by Django 4.1.3 on 2022-12-21 07:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('correlation', '0004_remove_categoryitemdata_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='categoryitemdata',
            old_name='strength',
            new_name='figure',
        ),
        migrations.RemoveField(
            model_name='categoryitemdata',
            name='existence',
        ),
    ]