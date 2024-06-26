# Generated by Django 4.2.7 on 2024-03-12 13:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0002_remove_product_product_group"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="price_number",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="product",
            name="type",
            field=models.IntegerField(choices=[(0, "Service"), (1, "Product")], default=1),
        ),
    ]
