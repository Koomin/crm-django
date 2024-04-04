# Generated by Django 4.2.7 on 2024-03-27 18:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shipping", "0002_shipping_default_send"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="shippingaddress",
            name="post",
        ),
        migrations.RemoveField(
            model_name="shippingaddress",
            name="state",
        ),
        migrations.AddField(
            model_name="shipping",
            name="is_sent",
            field=models.BooleanField(default=False),
        ),
    ]
