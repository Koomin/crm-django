from rest_framework import serializers

from crm.crm_config.api.serializers import CountrySerializer
from crm.crm_config.models import Country
from crm.service.api.serializers import AttributeDefinition, ServiceOrderSerializer
from crm.shipping.models import Shipping, ShippingAddress, ShippingStatus, Status


class StatusSerializer(serializers.ModelSerializer):
    attribute = serializers.SlugRelatedField(
        slug_field="uuid", queryset=AttributeDefinition.objects.all(), read_only=False
    )

    class Meta:
        model = Status
        fields = ["uuid", "code", "name", "attribute"]


class ShippingStatusSerializer(serializers.ModelSerializer):
    status = StatusSerializer(read_only=True)

    class Meta:
        model = ShippingStatus
        fields = ["uuid", "status", "date"]


class ShippingStatusRelatedSerializer(serializers.ModelSerializer):
    status = serializers.SlugRelatedField(slug_field="uuid", read_only=True)
    status_code = serializers.CharField(source="status.code", read_only=True)
    status_name = serializers.CharField(source="status.name", read_only=True)
    status_attribute = serializers.CharField(source="status.attribute.uuid", read_only=True)

    class Meta:
        model = ShippingStatus
        fields = ["uuid", "status", "status_code", "status_name", "status_attribute"]


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
    status = ShippingStatusRelatedSerializer(read_only=True)

    class Meta:
        model = Shipping
        fields = ["uuid", "service_order", "label", "track_ids", "default_send", "address", "is_sent", "status"]
