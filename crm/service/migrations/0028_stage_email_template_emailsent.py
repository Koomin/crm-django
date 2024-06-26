# Generated by Django 4.2.7 on 2024-03-07 16:24

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("crm_config", "0002_emailtemplate"),
        ("service", "0027_alter_serviceactivity_number_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="stage",
            name="email_template",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="crm_config.emailtemplate"
            ),
        ),
        migrations.CreateModel(
            name="EmailSent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uuid", models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("email", models.CharField(max_length=255)),
                ("subject", models.CharField(max_length=255)),
                ("message", models.TextField()),
                ("date_of_sent", models.DateTimeField(blank=True, null=True)),
                (
                    "email_template",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="emails_sent",
                        to="crm_config.emailtemplate",
                    ),
                ),
                (
                    "service_order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="emails_sent",
                        to="service.serviceorder",
                    ),
                ),
                (
                    "stage",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="emails_sent", to="service.stage"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
