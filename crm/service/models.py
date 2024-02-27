from django.db import models

from crm.contractors.models import Contractor
from crm.core.models import BaseModel, OptimaModel
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
    document_type = models.ForeignKey(DocumentType, on_delete=models.SET_NULL, null=True, blank=True)


class OrderType(BaseModel):
    name = models.CharField(max_length=50)


class ServiceOrder(OptimaModel):
    # Optima table - CDN.SrsZlecenia
    class States(models.IntegerChoices):
        ACCEPTED = 0, "Accepted"  # przyjęte Optima
        IN_REALIZATION = 1, "In realization"
        REALIZED = 2, "Realized"
        CANCELED = 3, "Canceled"
        NEW = 99, "New"

    document_type = models.ForeignKey(
        DocumentType, null=True, blank=False, related_name="service_order", on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category, null=True, blank=True, related_name="service_order", on_delete=models.CASCADE
    )
    number_scheme = models.CharField(max_length=255, null=True)
    number = models.IntegerField(null=True)
    full_number = models.CharField(max_length=255, null=True)
    status = models.BooleanField(default=False)
    state = models.IntegerField(choices=States.choices, default=States.NEW)
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE, null=True)
    contractor_type = models.IntegerField(null=True)
    contractor_name = models.CharField(max_length=1024, null=True)
    contractor_name1 = models.CharField(max_length=1024, null=True)
    contractor_name2 = models.CharField(max_length=1024, null=True)
    contractor_name3 = models.CharField(max_length=1024, null=True)
    contractor_city = models.CharField(max_length=120, null=True)
    contractor_country = models.CharField(max_length=50, null=True)
    contractor_street = models.CharField(max_length=200, null=True)
    contractor_street_number = models.CharField(max_length=12, null=True)
    contractor_home_number = models.IntegerField(null=True)
    contractor_state = models.CharField(max_length=40, null=True)
    contractor_post = models.CharField(max_length=120, null=True)
    contractor_postal_code = models.CharField(max_length=120, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    document_date = models.DateTimeField(null=True)
    acceptance_date = models.DateTimeField(null=True)
    realization_date = models.DateTimeField(null=True)
    closing_date = models.DateTimeField(null=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, null=True)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, null=True)
    net_value = models.DecimalField(decimal_places=2, max_digits=12, null=True)
    gross_value = models.DecimalField(decimal_places=2, max_digits=12, null=True)
    description = models.TextField()
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True)
    serial_number = models.CharField(max_length=255, null=True)
    purchase_document_number = models.CharField(max_length=255, null=True)
    purchase_date = models.DateField(null=True)
    email = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255, null=True)
    order_type = models.ForeignKey(OrderType, on_delete=models.CASCADE, null=True)
    purchase_document = models.FileField(upload_to="purchase_documents/", null=True, blank=True)


class Note(OptimaModel):
    # Optima table - CDN.SrsNotatki
    service_order = models.ForeignKey(ServiceOrder, on_delete=models.CASCADE)
    number = models.IntegerField()
    date = models.DateTimeField()
    description = models.TextField(max_length=1024)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class AttributeDefinition(OptimaModel):
    # Optima table - CDN.DefAtrybuty
    type = models.IntegerField()
    code = models.CharField(max_length=150)
    format = models.IntegerField()
    is_active = models.BooleanField(default=False)


class AttributeDefinitionItem(OptimaModel):
    # Optima table - CDN.DefAtrElem
    value = models.CharField(max_length=1000)
    number = models.IntegerField()
    attribute_definition = models.ForeignKey(AttributeDefinition, on_delete=models.CASCADE)


class Attribute(OptimaModel):
    # Optima table - CDN.DokAtrybuty
    attribute_definition = models.ForeignKey(AttributeDefinition, on_delete=models.CASCADE)
    code = models.CharField(max_length=150)
    value = models.CharField(max_length=1024)
    service_order = models.ForeignKey(ServiceOrder, on_delete=models.CASCADE, null=True)


class StageDuration(BaseModel):
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField()
    duration = models.DurationField()
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    service_order = models.ForeignKey(ServiceOrder, on_delete=models.CASCADE)

    def save(self):
        if self.start and self.end:
            self.duration = self.end - self.start
        super().save()


class FormFile(BaseModel):
    file = models.FileField(upload_to="form_files/")
    service_order = models.ForeignKey(ServiceOrder, on_delete=models.CASCADE, related_name="form_files")
