from django.db import models

from crm.core.models import OptimaModel


class ProductGroup(OptimaModel):
    # Optima table - CDN.TwrGrupy
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)


class Product(OptimaModel):
    # Optima table - CDN.Towary
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    unit = models.CharField(max_length=10)
