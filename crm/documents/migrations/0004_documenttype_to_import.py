# Generated by Django 4.2.7 on 2024-03-04 18:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("documents", "0003_documenttype_warehouse"),
    ]

    operations = [
        migrations.AddField(
            model_name="documenttype",
            name="to_import",
            field=models.BooleanField(default=False),
        ),
    ]