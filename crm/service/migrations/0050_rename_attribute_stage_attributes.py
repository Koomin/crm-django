# Generated by Django 4.2.7 on 2024-06-10 14:24

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("service", "0049_remove_stage_attribute_stage_attribute"),
    ]

    operations = [
        migrations.RenameField(
            model_name="stage",
            old_name="attribute",
            new_name="attributes",
        ),
    ]
