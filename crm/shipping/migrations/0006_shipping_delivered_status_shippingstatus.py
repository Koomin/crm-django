# Generated by Django 4.2.7 on 2024-04-02 18:12

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("service", "0036_alter_note_date_alter_note_number_and_more"),
        ("shipping", "0005_remove_shippingaddress_country_code_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="shipping",
            name="delivered",
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name="Status",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uuid", models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("code", models.CharField(max_length=25)),
                ("name", models.CharField(max_length=25)),
                (
                    "attribute",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="service.attributedefinition",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ShippingStatus",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uuid", models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("date", models.DateField(auto_now_add=True)),
                (
                    "shipping",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="status", to="shipping.shipping"
                    ),
                ),
                ("status", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="shipping.status")),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
