from django.contrib.postgres.fields import ArrayField
from django.db import models

from crm.core.models import BaseModel
from crm.crm_config.models import Country
from crm.service.models import AttributeDefinition, ServiceOrder
from crm.shipping.utils import GLSClient


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
    parcel_id = models.CharField(max_length=120, null=True, blank=True)
    parcel_number = models.CharField(max_length=120, null=True, blank=True)
    confirmation_id = models.CharField(max_length=120, null=True, blank=True)
    label = models.FileField(upload_to="labels", null=True, blank=True)
    track_ids = ArrayField(models.CharField(max_length=12, null=True, blank=True), null=True, blank=True)
    default_send = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)

    def send(self):
        if self.is_sent:
            return False
        client = GLSClient()
        created = client.create_parcel(self)
        if created:
            label_created = client.create_label(self)
            if label_created:
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
    date = models.DateField(auto_now_add=True)
    shipping = models.ForeignKey(Shipping, on_delete=models.CASCADE, related_name="status")
