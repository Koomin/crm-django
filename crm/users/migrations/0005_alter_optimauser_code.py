# Generated by Django 4.2.7 on 2024-01-18 09:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_optimauser_remove_user_optima_id_user_optima_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="optimauser",
            name="code",
            field=models.CharField(max_length=50, verbose_name="Code"),
        ),
    ]