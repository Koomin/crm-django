# Generated by Django 4.2.7 on 2024-08-01 11:54

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('crm_config', '0012_serviceaddress_opening_hours'),
    ]

    operations = [
        migrations.CreateModel(
            name='Import',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='imports/')),
                ('import_type', models.CharField(choices=[('Shipping Methods', 'Shipping Methods')], default='Shipping Methods', max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
