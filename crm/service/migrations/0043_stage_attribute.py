# Generated by Django 4.2.7 on 2024-05-09 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("service", "0042_device_shipping_company"),
    ]

    operations = [
        migrations.AddField(
            model_name="stage",
            name="attribute",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="service.attribute"
            ),
        ),
    ]
