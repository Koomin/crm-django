import datetime

from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist, ValidationError
from django.db import models

from crm.core.models import BaseModel
from crm.crm_config.models import Country, Log
from crm.service.models import AttributeDefinition, ServiceOrder
from crm.shipping.utils import GLSClient, RabenClient


class ShippingCompany(BaseModel):
    class Companies(models.TextChoices):
        GLS = "GLS", "GLS"
        RABEN = "RABEN", "Raben"

    name = models.CharField(choices=Companies.choices, default=Companies.GLS)

    def save(self, *args, **kwargs):
        if self._state.adding:
            if ShippingCompany.objects.filter(name=self.name).exists():
                raise ValidationError("Company has to be unique")
        super().save(*args, **kwargs)


class ShippingMethod(BaseModel):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(ShippingCompany, on_delete=models.CASCADE, related_name="methods")
    code = models.CharField(max_length=15, null=True, blank=True)


class ShippingAddress(BaseModel):
    name = models.CharField(max_length=1024, null=True, blank=True)
    city = models.CharField(max_length=120, null=True, blank=True)
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.CASCADE)
    street = models.CharField(max_length=200, null=True, blank=True)
    street_number = models.CharField(max_length=12, null=True, blank=True)
    home_number = models.IntegerField(null=True, blank=True)
    postal_code = models.CharField(max_length=120, null=True, blank=True)


class Shipping(BaseModel):
    address = models.OneToOneField(ShippingAddress, on_delete=models.CASCADE, related_name="shipping")
    service_order = models.OneToOneField(ServiceOrder, on_delete=models.CASCADE, related_name="shipping")
    shipping_company = models.ForeignKey(
        ShippingCompany, on_delete=models.CASCADE, related_name="shipping", null=True, blank=True
    )
    shipping_method = models.ForeignKey(
        ShippingMethod, on_delete=models.CASCADE, related_name="shipping", null=True, blank=True
    )
    parcel_id = models.CharField(max_length=120, null=True, blank=True)
    parcel_number = models.CharField(max_length=120, null=True, blank=True)
    confirmation_id = models.CharField(max_length=120, null=True, blank=True)
    label = models.FileField(upload_to="labels", null=True, blank=True)
    track_ids = ArrayField(models.CharField(max_length=12, null=True, blank=True), null=True, blank=True)
    default_send = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.shipping_method and not self.shipping_company:
            self.shipping_company = self.shipping_method.company
        super().save(*args, **kwargs)

    def send(self):
        if self.is_sent:
            return False
        if self.shipping_company.name == "GLS":
            client = GLSClient()
        elif self.shipping_company.name == "RABEN":
            client = RabenClient()
        else:
            Log.objects.create(
                exception_traceback="No shipping company",
                method_name="send",
                model_name=self.model.__name__,
                object_uuid=self.uuid,
            )
            return False
        created = client.create_parcel(self)
        if created:
            # GLS PR shipping method - cannot generate label
            # label_created = client.create_label(self)
            # if label_created:
            confirmed = client.confirm_shipping(self)
            if confirmed:
                self.is_sent = True
                self.save_without_update()
                client.logout()
                return True
        client.logout()
        return False


class Status(BaseModel):
    code = models.CharField(max_length=25)
    name = models.CharField(max_length=25)
    attribute = models.ForeignKey(AttributeDefinition, on_delete=models.CASCADE, null=True, blank=True)


class ShippingStatus(BaseModel):
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    date = models.DateField()
    shipping = models.ForeignKey(Shipping, on_delete=models.CASCADE, related_name="status")

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.date = datetime.date.today()
            if self.status.attribute:
                try:
                    attribute = self.shipping.service_order.attributes.get(attribute_definition=self.status.attribute)
                except (ObjectDoesNotExist, MultipleObjectsReturned) as e:
                    Log.objects.create(
                        exception_traceback=e,
                        method_name="save",
                        model_name=self.__class__.__name__,
                        object_uuid=self.uuid,
                    )
                else:
                    attribute.value = self.date
                    attribute.save()
        super().save(*args, **kwargs)
