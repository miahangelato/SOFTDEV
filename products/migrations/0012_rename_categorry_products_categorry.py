# Generated by Django 5.1.1 on 2024-09-27 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_products_categorry'),
    ]

    operations = [
        migrations.RenameField(
            model_name='products',
            old_name='Categorry',
            new_name='categorry',
        ),
    ]
