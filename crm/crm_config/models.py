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


class EmailTemplate(BaseModel):
    name = models.CharField(max_length=255)
    template = models.TextField()
    subject = models.CharField(max_length=255)
