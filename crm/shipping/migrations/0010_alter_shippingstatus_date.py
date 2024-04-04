# Generated by Django 4.2.7 on 2024-04-04 18:51

from django.db import migrations, models


def fill_date(apps, schema_editor):
    import datetime
    shippingstatus = apps.get_model('shipping', 'shippingstatus')
    shippingstatus.objects.filter(date__isnull=True).update(date=datetime.date.today())


class Migration(migrations.Migration):
    dependencies = [
        ("shipping", "0009_alter_shippingstatus_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shippingstatus",
            name="date",
            field=models.DateField(null=True),
        ),
        migrations.RunPython(fill_date)
    ]