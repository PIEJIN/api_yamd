# Generated by Django 3.2 on 2023-04-16 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0006_auto_20230416_0625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='raiting',
            field=models.FloatField(blank=True),
        ),
    ]
