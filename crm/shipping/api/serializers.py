from rest_framework import serializers

from crm.service.api.serializers import ServiceOrderSerializer
from crm.shipping.models import Shipping, ShippingAddress


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ["uuid", "name", "city", "country", "postal_code", "street", "street_number", "home_number"]


class ShippingSerializer(serializers.ModelSerializer):
    address = ShippingAddressSerializer(read_only=True)
    service_order = ServiceOrderSerializer(read_only=True)

    class Meta:
        model = Shipping
        fields = ["uuid", "service_order", "label", "track_ids", "default_send", "address", "is_sent"]
