from django.db import models

from crm.contractors.models import Contractor
from crm.core.models import BaseModel, OptimaModel
from crm.crm_config.models import EmailTemplate, Log
from crm.documents.models import DocumentType
from crm.products.models import Product
from crm.users.models import OptimaUser, User
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
    email_template = models.ForeignKey(EmailTemplate, on_delete=models.CASCADE, null=True)
    is_default = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        Stage.objects.filter(is_default=True).update(is_default=False)
        super().save(*args, **kwargs)


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
    number_scheme = models.CharField(max_length=255, null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)
    full_number = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=False, blank=True)
    state = models.IntegerField(choices=States.choices, default=States.NEW)
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE, null=True, blank=True)
    contractor_type = models.IntegerField(null=True, blank=True)
    contractor_name = models.CharField(max_length=1024, null=True, blank=True)
    contractor_name1 = models.CharField(max_length=1024, null=True, blank=True)
    contractor_name2 = models.CharField(max_length=1024, null=True, blank=True)
    contractor_name3 = models.CharField(max_length=1024, null=True, blank=True)
    contractor_city = models.CharField(max_length=120, null=True, blank=True)
    contractor_country = models.CharField(max_length=50, null=True, blank=True)
    contractor_street = models.CharField(max_length=200, null=True, blank=True)
    contractor_street_number = models.CharField(max_length=12, null=True, blank=True)
    contractor_home_number = models.IntegerField(null=True, blank=True)
    contractor_state = models.CharField(max_length=40, null=True, blank=True)
    contractor_post = models.CharField(max_length=120, null=True, blank=True)
    contractor_postal_code = models.CharField(max_length=120, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    document_date = models.DateTimeField(null=True, blank=True)
    acceptance_date = models.DateTimeField(null=True, blank=True)
    realization_date = models.DateTimeField(null=True, blank=True)
    closing_date = models.DateTimeField(null=True, blank=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, null=True, blank=True)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, null=True, blank=True)
    net_value = models.DecimalField(decimal_places=2, max_digits=12, null=True, blank=True)
    gross_value = models.DecimalField(decimal_places=2, max_digits=12, null=True, blank=True)
    description = models.TextField()
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True, blank=True)
    serial_number = models.CharField(max_length=255, null=True, blank=True)
    purchase_document_number = models.CharField(max_length=255, null=True, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    order_type = models.ForeignKey(OrderType, on_delete=models.CASCADE, null=True, blank=True)
    purchase_document = models.FileField(upload_to="purchase_documents/", null=True, blank=True)

    # TODO Fill contractor_name1 etc while saving
    def _export_to_optima(self) -> (bool, str, dict):
        from service.optima_api.serializers import ServiceOrderSerializer
        from service.optima_api.views import ServiceOrderObject

        from crm.service.tasks import synchronize_order

        if self.state != self.States.NEW:
            if not self.number:
                last_number = max(
                    ServiceOrder.objects.filter(
                        document_type=self.document_type,
                        optima_id__isnull=False,
                        number_scheme=self.number_scheme,
                        number__isnull=False,
                    ).values_list("number", flat=True)
                )
                if not last_number:
                    last_number = 0
                optima_last_number = ServiceOrderObject().get_last_number(
                    self.number_scheme, self.document_type.optima_id, last_number
                )
                print(optima_last_number)
                if optima_last_number:
                    self.number = optima_last_number + 1
                else:
                    self.number = 1
            serializer = ServiceOrderSerializer(self)
            if serializer.is_valid(safe=False):
                optima_object = ServiceOrderObject()
                created, response = optima_object.post(serializer.data)
                if created and response:
                    self.optima_id = response
                    self.exported = True
                    super().save()
                    synchronize_order.apply_async(args=[str(self.optima_id)])
                return created, response, serializer.data
            return False, serializer.errors, {}
        return False, None, {}

    def export(self):
        if not self.exported and not self.optima_id:
            created, errors, data = self._export_to_optima()
            if not created:
                Log.objects.create(
                    exception_traceback=",".join(errors),
                    method_name="export",
                    model_name=self.__class__.__name__,
                    object_uuid=self.uuid,
                    object_serialized=data,
                )
            return True
        return False

    def _update_optima_obj(self):
        try:
            from service.optima_api.serializers import ServiceOrderSerializer
            from service.optima_api.views import ServiceOrderObject
        except ModuleNotFoundError:
            from crm.service.optima_api.serializers import ServiceOrderSerializer
            from crm.service.optima_api.views import ServiceOrderObject

        if self.state != self.States.NEW:
            serializer = ServiceOrderSerializer(self)
            if serializer.is_valid(safe=False):
                optima_object = ServiceOrderObject()
                updated, response = optima_object.put(serializer.data, self.optima_id)
                return updated, response, serializer.data
            return False, serializer.errors, {}


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


class ServicePart(OptimaModel):
    # Optima table - CDN.SrsCzesci
    service_order = models.ForeignKey(ServiceOrder, on_delete=models.CASCADE, related_name="service_parts")
    number = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="service_parts")
    to_invoicing = models.BooleanField(default=False)
    user = models.ForeignKey(OptimaUser, on_delete=models.CASCADE, related_name="service_parts")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="service_parts")
    price_net = models.DecimalField(max_digits=10, decimal_places=2)
    price_gross = models.DecimalField(max_digits=10, decimal_places=2)
    price_discount = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_collected = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_released = models.DecimalField(max_digits=10, decimal_places=2)
    status_collected = models.IntegerField()
    unit = models.CharField(max_length=10)
    to_return = models.BooleanField(default=False)
    document = models.IntegerField()


class ServiceActivity(OptimaModel):
    # Optima table - CDN.SrsCzynnosci
    service_order = models.ForeignKey(ServiceOrder, on_delete=models.CASCADE, related_name="service_activities")
    number = models.IntegerField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="service_activities")
    user = models.ForeignKey(OptimaUser, on_delete=models.CASCADE, related_name="service_activities")
    is_finished = models.BooleanField(default=False)
    to_invoicing = models.BooleanField(default=False)
    date_of_service = models.DateTimeField(null=True, blank=True)
    date_from = models.DateTimeField(null=True, blank=True)
    date_to = models.DateTimeField(null=True, blank=True)
    price_net = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_gross = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    value_net = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    value_gross = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    unit = models.CharField(max_length=10, null=True, blank=True)


class EmailSent(BaseModel):
    email = models.CharField(max_length=255, null=False)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name="emails_sent")
    email_template = models.ForeignKey(EmailTemplate, on_delete=models.CASCADE, related_name="emails_sent")
    subject = models.CharField(max_length=255)
    message = models.TextField()
    date_of_sent = models.DateTimeField(null=True, blank=True)
    service_order = models.ForeignKey(ServiceOrder, on_delete=models.CASCADE, related_name="emails_sent")
