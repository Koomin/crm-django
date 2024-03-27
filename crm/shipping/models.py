from django.contrib.postgres.fields import ArrayField
from django.db import models

from crm.core.models import BaseModel
from crm.service.models import ServiceOrder
from crm.shipping.utils import GLSClient


class ShippingAddress(BaseModel):
    name = models.CharField(max_length=1024, null=True, blank=True)
    city = models.CharField(max_length=120, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    country_code = models.CharField(max_length=5, null=False, blank=False)
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
                    return True
        return False
