# Generated by Django 5.0.2 on 2024-02-18 22:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='manufacturer',
            options={'ordering': ['name'], 'verbose_name': 'Manufacturer', 'verbose_name_plural': 'Manufacturers'},
        ),
        migrations.AlterModelOptions(
            name='warehouse',
            options={'ordering': ['name'], 'verbose_name': 'Warehouse', 'verbose_name_plural': 'Warehouses'},
        ),
    ]