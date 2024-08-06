import csv

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models

from crm.core.models import BaseModel, OptimaModel


class Country(OptimaModel):
    # Optima table - CDN.Kraje
    name = models.CharField(max_length=255)
    code = models.CharField(unique=True, max_length=2)


class State(OptimaModel):
    # Optima table - CDN.Teryt
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)


class ServiceAddress(BaseModel):
    name = models.CharField(max_length=1024, null=True, blank=True)
    city = models.CharField(max_length=120, null=True, blank=True)
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.CASCADE)
    street = models.CharField(max_length=200, null=True, blank=True)
    street_number = models.CharField(max_length=12, null=True, blank=True)
    home_number = models.IntegerField(null=True, blank=True)
    postal_code = models.CharField(max_length=120, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    opening_hours = models.TextField(null=True, blank=True)


class TaxPercentage(BaseModel):
    name = models.CharField(max_length=12)
    value = models.DecimalField(max_digits=4, decimal_places=2)


class EmailTemplate(BaseModel):
    name = models.CharField(max_length=255)
    template = models.TextField()
    subject = models.CharField(max_length=255)


class GeneralSettings(BaseModel):
    optima_synchronization = models.BooleanField(default=False)
    mailing = models.BooleanField(default=False)
    optima_config_database = models.CharField(max_length=255, null=True, blank=True)
    optima_general_database = models.CharField(max_length=255, null=True, blank=True)
    admin_email = models.EmailField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk and GeneralSettings.objects.exists():
            raise ValidationError("Only one settings can be saved")
        super().save(*args, **kwargs)


class Log(BaseModel):
    class Status(models.IntegerChoices):
        ERROR = 0, "Error"
        INFO = 1, "Info"

    number = models.IntegerField(unique=True)
    exception_traceback = models.TextField(null=True, blank=True)
    method_name = models.CharField(max_length=255)
    model_name = models.CharField(max_length=255, null=True)
    object_uuid = models.UUIDField(null=True)
    object_serialized = models.TextField(null=True, blank=True)
    status = models.IntegerField(choices=Status.choices, default=Status.ERROR)

    def save(self, *args, **kwargs):
        if not self.pk:
            if Log.objects.exists():
                self.number = Log.objects.last().number + 1
            else:
                self.number = 1
        super().save(*args, **kwargs)


class Import(BaseModel):
    class ImportType(models.TextChoices):
        shipping_methods = "Shipping Methods", "Shipping Methods"

    file = models.FileField(blank=True, null=True, upload_to="imports/")
    import_type = models.CharField(max_length=255, choices=ImportType.choices, default=ImportType.shipping_methods)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.import_type == "Shipping Methods":
            with open(self.file.file.name, encoding="utf-8", errors="ignore") as f:
                data = csv.reader(f, delimiter=";")
                from crm.service.models import Device
                from crm.shipping.models import ShippingMethod

                for idx, row in enumerate(data):
                    if idx == 0:
                        continue
                    if row[0]:
                        device_code = row[0]
                        shipping_methods = row[3].replace(" ", "").split(",")
                        try:
                            device = Device.objects.get(code=device_code)
                        except ObjectDoesNotExist:
                            pass
                        else:
                            device.shipping_method.set(ShippingMethod.objects.filter(name__in=shipping_methods))
