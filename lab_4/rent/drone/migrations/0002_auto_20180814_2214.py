# Generated by Django 2.0.7 on 2018-08-14 20:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drone', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Galery',
            new_name='Gallery',
        ),
        migrations.AlterModelTable(
            name='gallery',
            table='gallery',
        ),
    ]
