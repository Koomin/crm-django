# Generated by Django 4.2.7 on 2024-04-04 18:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("contractors", "0007_alter_contractor_code_alter_contractor_home_number_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contractor",
            name="country",
            field=models.CharField(max_length=250),
        ),
    ]