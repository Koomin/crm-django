# Generated by Django 4.2.7 on 2024-02-19 17:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0005_alter_optimauser_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="created",
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
