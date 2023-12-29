from rest_framework import serializers

from crm.service.models import Category, Device, DeviceType, ServiceOrder, Stage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["uuid", "code", "code_detailed", "description"]


class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ["uuid", "type", "code", "description"]


class DeviceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = ["uuid", "code", "active", "name"]


class DeviceSerializer(serializers.ModelSerializer):
    device_type = serializers.SlugRelatedField(slug_field="uuid", read_only=True)

    class Meta:
        model = Device
        fields = ["uuid", "code", "name", "description", "device_type"]


class ServiceOrderSerializer(serializers.ModelSerializer):
    document_type = serializers.SlugRelatedField(slug_field="uuid", read_only=True)
    category = serializers.SlugRelatedField(slug_field="uuid", read_only=True)
    contractor = serializers.SlugRelatedField(slug_field="uuid", read_only=True)
    user = serializers.SlugRelatedField(slug_field="uuid", read_only=True)
    warehouse = serializers.SlugRelatedField(slug_field="uuid", read_only=True)
    stage = serializers.SlugRelatedField(slug_field="uuid", read_only=True)
    device = serializers.SlugRelatedField(slug_field="uuid", read_only=True)

    class Meta:
        model = ServiceOrder
        fields = [
            "uuid",
            "document_type",
            "category",
            "number_scheme",
            "number",
            "status",
            "state",
            "contractor",
            "user",
            "document_date",
            "acceptance_date",
            "realization_date",
            "closing_date",
            "warehouse",
            "stage",
            "net_value",
            "gross_value",
            "description",
            "device",
        ]
