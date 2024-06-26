# Generated by Django 4.2.7 on 2024-03-07 19:19

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("crm_config", "0003_emailtemplate_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="GeneralSettings",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uuid", models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("optima_synchronization", models.BooleanField(default=False)),
                ("mailing", models.BooleanField(default=False)),
                ("optima_config_database", models.CharField(max_length=255)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
