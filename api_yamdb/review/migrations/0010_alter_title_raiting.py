# Generated by Django 3.2 on 2023-04-16 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0009_alter_title_raiting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='raiting',
            field=models.FloatField(default=0, null=True),
        ),
    ]
