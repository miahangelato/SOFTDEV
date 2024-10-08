# Generated by Django 5.1.1 on 2024-09-27 10:53

import products.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_rename_categorry_products_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='products',
            name='category',
            field=models.CharField(max_length=100, verbose_name=products.models.Category),
        ),
    ]
