# Generated by Django 4.2.7 on 2024-03-12 11:04

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("crm_config", "0007_log_number"),
    ]

    operations = [
        migrations.CreateModel(
            name="TaxPercentage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uuid", models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=12)),
                ("value", models.DecimalField(decimal_places=2, max_digits=4)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
