# Generated by Django 4.2.7 on 2024-07-15 18:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shipping", "0016_shipping_shipping_method"),
    ]

    operations = [
        migrations.AddField(
            model_name="shippingmethod",
            name="code",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
