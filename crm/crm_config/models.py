from django.core.exceptions import ValidationError
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
