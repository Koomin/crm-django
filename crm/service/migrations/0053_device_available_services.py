# Generated by Django 4.2.7 on 2024-08-01 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_config', '0012_serviceaddress_opening_hours'),
        ('service', '0052_remove_device_shipping_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='available_services',
            field=models.ManyToManyField(blank=True, to='crm_config.serviceaddress'),
        ),
    ]
