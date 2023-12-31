# Generated by Django 4.2.4 on 2023-09-07 05:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('correlation', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonthlyMean',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=200)),
                ('mean', models.DecimalField(decimal_places=2, max_digits=5)),
                ('target_year', models.IntegerField(default=2023)),
                ('target_month', models.IntegerField(null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category_item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='correlation.categoryitem')),
            ],
        ),
    ]
