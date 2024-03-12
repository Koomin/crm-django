from django.db import models

from crm.core.models import OptimaModel


class ProductGroup(OptimaModel):
    # Optima table - CDN.TwrGrupy
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)


class Product(OptimaModel):
    # Optima table - CDN.Towary
    class ProductType(models.IntegerChoices):
        SERVICE = 0, "Service"
        PRODUCT = 1, "Product"

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    unit = models.CharField(max_length=10)
    type = models.IntegerField(choices=ProductType.choices, default=ProductType.PRODUCT)
    price_number = models.IntegerField(default=0)
