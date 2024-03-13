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

    def save(self, *args, **kwargs):
        if not self.pk and GeneralSettings.objects.exists():
            return ValidationError("Only one settings can be saved")
        return super().save(*args, **kwargs)


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
