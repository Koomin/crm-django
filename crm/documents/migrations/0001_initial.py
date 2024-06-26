# Generated by Django 4.2.7 on 2023-12-20 18:13

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DocumentType",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uuid", models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("optima_id", models.IntegerField(blank=True, null=True)),
                ("exported", models.BooleanField(default=False)),
                ("symbol", models.CharField(max_length=12)),
                ("obj_class", models.IntegerField()),
                ("name", models.CharField(max_length=255)),
                ("numbering_scheme", models.CharField(max_length=500)),
                ("active", models.BooleanField(default=True)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
