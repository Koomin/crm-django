# Generated by Django 4.2.7 on 2024-03-07 16:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("crm_config", "0002_emailtemplate"),
    ]

    operations = [
        migrations.AddField(
            model_name="emailtemplate",
            name="name",
            field=models.CharField(default="", max_length=255),
            preserve_default=False,
        ),
    ]
