# Generated by Django 4.2.7 on 2024-03-14 13:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("service", "0035_emailsent_sent"),
    ]

    operations = [
        migrations.AlterField(
            model_name="note",
            name="date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="note",
            name="number",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="note",
            name="service_order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="notes", to="service.serviceorder"
            ),
        ),
    ]
