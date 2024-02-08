# Generated by Django 4.2.7 on 2024-01-20 13:15

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("service", "0008_serviceorder_contractor_city_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="OrderType",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uuid", models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=50)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]