# Generated by Django 4.2.7 on 2023-12-20 18:13

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Contractor",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uuid", models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("optima_id", models.IntegerField(blank=True, null=True)),
                ("exported", models.BooleanField(default=False)),
                ("code", models.CharField(max_length=120)),
                ("postal_code", models.CharField(max_length=6)),
                ("tax_number", models.CharField(max_length=30)),
                ("phone_number", models.CharField(max_length=15)),
                ("country", models.CharField(max_length=50)),
                ("city", models.CharField(max_length=120)),
                ("street", models.CharField(max_length=200)),
                ("street_number", models.CharField(max_length=12)),
                ("home_number", models.IntegerField()),
                ("post", models.CharField(max_length=120)),
                ("state", models.CharField(max_length=40)),
                ("name", models.CharField(max_length=1024)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
