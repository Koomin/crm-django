# Generated by Django 4.2.7 on 2024-03-27 15:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shipping", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="shipping",
            name="default_send",
            field=models.BooleanField(default=False),
        ),
    ]