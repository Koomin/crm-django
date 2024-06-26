# Generated by Django 4.2.7 on 2024-05-09 17:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("shipping", "0013_shipping_shipping_company"),
        ("products", "0004_product_active"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="shipping_company",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="shipping.shippingcompany"
            ),
        ),
    ]
