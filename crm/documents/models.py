from django.db import models

from crm.core.models import OptimaModel
from crm.warehouses.models import Warehouse


class DocumentType(OptimaModel):
    # Optima table - CDN.DokDefinicje
    symbol = models.CharField(null=False, max_length=12)
    obj_class = models.IntegerField(null=False)
    name = models.CharField(null=False, max_length=255)
    numbering_scheme = models.CharField(null=False, max_length=500)
    active = models.BooleanField(default=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, blank=True)
