# Generated by Django 4.2.7 on 2024-05-09 19:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("service", "0043_stage_attribute"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stage",
            name="attribute",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="service.attributedefinition"
            ),
        ),
    ]
