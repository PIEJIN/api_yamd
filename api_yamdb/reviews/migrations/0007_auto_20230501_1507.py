# Generated by Django 3.2 on 2023-05-01 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_auto_20230501_1413'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='title',
            constraint=models.CheckConstraint(check=models.Q(year__lte=2023), name='year_lte_current_year'),
        ),
        migrations.AddConstraint(
            model_name='title',
            constraint=models.CheckConstraint(check=models.Q(year__gte=0), name='year_gte_minimum_year'),
        ),
    ]