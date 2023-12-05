from django.db import models

from crm.contractors.models import Contractor
from crm.core.models import OptimaModel
from crm.documents.models import DocumentType
from crm.users.models import User
from crm.warehouses.models import Warehouse


class Category(OptimaModel):
    code = models.CharField(max_length=255)
    code_detailed = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)


class Stage(OptimaModel):
    # Optima table - CDN.DefEtapy
    type = models.IntegerField()
    code = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=255, null=True)


class DeviceType(OptimaModel):
    # Optima table - CDN.SrsRodzajeU
    code = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=255)


class Device(OptimaModel):
    # Optima table - CDN.SrsUrzadzenia
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)


class ServiceOrder(OptimaModel):
    # Optima table - CDN.SrsZlecenia
    class States(models.IntegerChoices):
        ACCEPTED = 0, "Accepted"
        IN_REALIZATION = 1, "In realization"
        REALIZED = 2, "Realized"

    document_type = models.ForeignKey(
        DocumentType, null=False, blank=False, related_name="service_order", on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category, null=True, blank=True, related_name="service_order", on_delete=models.CASCADE
    )
    number_scheme = models.CharField(max_length=255)
    number = models.IntegerField()
    status = models.BooleanField(default=False)
    state = models.IntegerField(choices=States.choices, default=States.ACCEPTED)
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document_date = models.DateTimeField()
    acceptance_date = models.DateTimeField()
    realization_date = models.DateTimeField()
    closing_date = models.DateTimeField()
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    net_value = models.DecimalField(decimal_places=2, max_digits=12)
    gross_value = models.DecimalField(decimal_places=2, max_digits=12)
    description = models.TextField()
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
