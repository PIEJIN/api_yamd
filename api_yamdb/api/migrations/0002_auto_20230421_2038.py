# Generated by Django 3.2 on 2023-04-21 12:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Genre',
        ),
        migrations.DeleteModel(
            name='Genre_title',
        ),
        migrations.DeleteModel(
            name='Titles',
        ),
        migrations.DeleteModel(
            name='Users',
        ),
    ]
