# Generated by Django 4.2.7 on 2024-01-20 15:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("service", "0010_serviceorder_purchase_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="serviceorder",
            name="gross_value",
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name="serviceorder",
            name="net_value",
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True),
        ),
    ]
