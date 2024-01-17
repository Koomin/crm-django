from rest_framework import serializers

from crm.contractors.models import Contractor
from crm.documents.models import DocumentType
from crm.service.models import Category, Device, DeviceType, ServiceOrder, Stage
from crm.warehouses.models import Warehouse


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
    document_type = serializers.SlugRelatedField(
        slug_field="uuid", queryset=DocumentType.objects.all(), read_only=False
    )
    document_type_name = serializers.CharField(source="document_type.symbol", allow_null=True, required=False)
    category = serializers.SlugRelatedField(slug_field="uuid", queryset=Category.objects.all(), read_only=False)
    category_code = serializers.CharField(source="category.code", allow_null=True, required=False)
    contractor = serializers.SlugRelatedField(slug_field="uuid", queryset=Contractor.objects.all(), read_only=False)
    contractor_name = serializers.CharField(source="contractor.name", allow_null=True, required=False)
    user = serializers.SlugRelatedField(slug_field="uuid", read_only=True)
    warehouse = serializers.SlugRelatedField(slug_field="uuid", queryset=Warehouse.objects.all(), read_only=False)
    warehouse_name = serializers.CharField(source="warehouse.name", allow_null=True, required=False)
    warehouse_symbol = serializers.CharField(source="warehouse.symbol", allow_null=True, required=False)
    stage = serializers.SlugRelatedField(slug_field="uuid", queryset=Stage.objects.all(), read_only=False)
    device = serializers.SlugRelatedField(slug_field="uuid", queryset=Device.objects.all(), read_only=False)
    document_date_formatted = serializers.DateTimeField(source="document_date", format="%Y-%m-%d", required=False)
    acceptance_date_formatted = serializers.DateTimeField(source="acceptance_date", format="%Y-%m-%d", required=False)
    realization_date_formatted = serializers.DateTimeField(
        source="realization_date", format="%Y-%m-%d", required=False
    )
    closing_date_formatted = serializers.DateTimeField(source="closing", format="%Y-%m-%d", required=False)
    device_name = serializers.CharField(source="device.name", allow_null=True, required=False)
    device_code = serializers.CharField(source="device.code", allow_null=True, required=False)

    class Meta:
        model = ServiceOrder
        fields = [
            "uuid",
            "document_type",
            "document_type_name",
            "category",
            "category_code",
            "number_scheme",
            "number",
            "full_number",
            "status",
            "state",
            "contractor",
            "contractor_name",
            "user",
            "document_date",
            "document_date_formatted",
            "acceptance_date",
            "acceptance_date_formatted",
            "realization_date",
            "realization_date_formatted",
            "closing_date",
            "closing_date_formatted",
            "warehouse",
            "warehouse_name",
            "warehouse_symbol",
            "stage",
            "net_value",
            "gross_value",
            "description",
            "device",
            "device_name",
            "device_code",
        ]
