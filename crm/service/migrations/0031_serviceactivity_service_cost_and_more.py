# Generated by Django 4.2.7 on 2024-03-12 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("crm_config", "0008_taxpercentage"),
        ("service", "0030_stage_is_default"),
    ]

    operations = [
        migrations.AddField(
            model_name="serviceactivity",
            name="service_cost",
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name="serviceactivity",
            name="tax_percentage",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="crm_config.taxpercentage"
            ),
        ),
    ]
