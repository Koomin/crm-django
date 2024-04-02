from rest_framework import serializers

from crm.crm_config.api.serializers import CountrySerializer
from crm.crm_config.models import Country
from crm.service.api.serializers import AttributeDefinition, ServiceOrderSerializer
from crm.shipping.models import Shipping, ShippingAddress, Status


class ShippingAddressSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=False)

    class Meta:
        model = ShippingAddress
        fields = ["uuid", "name", "city", "country", "postal_code", "street", "street_number", "home_number"]


class ShippingAddressUpdateSerializer(serializers.ModelSerializer):
    country = serializers.SlugRelatedField(slug_field="uuid", queryset=Country.objects.all(), read_only=False)

    class Meta:
        model = ShippingAddress
        fields = ["name", "city", "country", "postal_code", "street", "street_number", "home_number"]


class ShippingSerializer(serializers.ModelSerializer):
    address = ShippingAddressSerializer(read_only=True)
    service_order = ServiceOrderSerializer(read_only=True)

    class Meta:
        model = Shipping
        fields = ["uuid", "service_order", "label", "track_ids", "default_send", "address", "is_sent"]


class StatusSerializer(serializers.ModelSerializer):
    attribute = serializers.SlugRelatedField(
        slug_field="uuid", queryset=AttributeDefinition.objects.all(), read_only=False
    )

    class Meta:
        model = Status
        fields = ["uuid", "code", "name", "attribute"]
