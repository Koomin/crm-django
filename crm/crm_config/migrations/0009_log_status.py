# Generated by Django 4.2.7 on 2024-03-13 12:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("crm_config", "0008_taxpercentage"),
    ]

    operations = [
        migrations.AddField(
            model_name="log",
            name="status",
            field=models.IntegerField(choices=[(0, "Error"), (1, "Info")], default=0),
        ),
    ]
