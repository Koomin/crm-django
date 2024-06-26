# Generated by Django 4.2.7 on 2024-05-09 17:15

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("shipping", "0011_alter_shippingstatus_date"),
    ]

    operations = [
        migrations.CreateModel(
            name="ShippingCompany",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uuid", models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(choices=[("GLS", "GLS"), ("RABEN", "Raben")], default="GLS")),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
