from django.db import models

from crm.contractors.models import Contractor
from crm.core.models import OptimaModel
from crm.documents.models import DocumentType
from crm.users.models import User
from crm.warehouses.models import Warehouse


class Category(OptimaModel):
    # Optima table - CDN.Kategorie
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
        ACCEPTED = 0, "Accepted"  # przyjęte Optima
        IN_REALIZATION = 1, "In realization"
        REALIZED = 2, "Realized"
        CANCELED = 3, "Canceled"
        NEW = 99, "New"

    document_type = models.ForeignKey(
        DocumentType, null=False, blank=False, related_name="service_order", on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category, null=True, blank=True, related_name="service_order", on_delete=models.CASCADE
    )
    number_scheme = models.CharField(max_length=255)
    number = models.IntegerField()
    full_number = models.CharField(max_length=255, null=True)
    status = models.BooleanField(default=False)
    state = models.IntegerField(choices=States.choices, default=States.ACCEPTED)
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE, null=True)
    contractor_type = models.IntegerField(null=True)
    contractor_name = models.CharField(max_length=1024)
    contractor_name1 = models.CharField(max_length=1024)
    contractor_name2 = models.CharField(max_length=1024)
    contractor_name3 = models.CharField(max_length=1024)
    contractor_city = models.CharField(max_length=120)
    contractor_country = models.CharField(max_length=50)
    contractor_street = models.CharField(max_length=200)
    contractor_street_number = models.CharField(max_length=12)
    contractor_home_number = models.IntegerField(null=True)
    contractor_state = models.CharField(max_length=40)
    contractor_post = models.CharField(max_length=120)
    contractor_postal_code = models.CharField(max_length=120)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    document_date = models.DateTimeField(null=True)
    acceptance_date = models.DateTimeField(null=True)
    realization_date = models.DateTimeField(null=True)
    closing_date = models.DateTimeField(null=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, null=True)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, null=True)
    net_value = models.DecimalField(decimal_places=2, max_digits=12)
    gross_value = models.DecimalField(decimal_places=2, max_digits=12)
    description = models.TextField()
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True)
    email = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255, null=True)


class Note(OptimaModel):
    # Optima table - CDN.SrsNotatki
    service_order = models.ForeignKey(ServiceOrder, on_delete=models.CASCADE)
    number = models.IntegerField()
    date = models.DateTimeField()
    description = models.TextField(max_length=1024)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
