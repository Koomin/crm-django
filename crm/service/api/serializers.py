from rest_framework import serializers

from crm.contractors.models import Contractor
from crm.documents.models import DocumentType
from crm.service.models import Category, Device, DeviceType, ServiceOrder, Stage
from crm.users.models import User
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
    device_type_uuid = serializers.SlugRelatedField(slug_field="uuid", queryset=DeviceType.objects.all())

    class Meta:
        model = Device
        fields = ["uuid", "code", "name", "description", "device_type_uuid"]


class ServiceOrderSerializer(serializers.ModelSerializer):
    document_type_uuid = serializers.SlugRelatedField(slug_field="uuid", queryset=DocumentType.objects.all())
    category_uuid = serializers.SlugRelatedField(slug_field="uuid", queryset=Category.objects.all())
    contractor_uuid = serializers.SlugRelatedField(slug_field="uuid", queryset=Contractor.objects.all())
    user_uuid = serializers.SlugRelatedField(slug_field="uuid", queryset=User.objects.all())
    warehouse_uuid = serializers.SlugRelatedField(slug_field="uuid", queryset=Warehouse.objects.all())
    stage_uuid = serializers.SlugRelatedField(slug_field="uuid", queryset=Stage.objects.all())
    device_uuid = serializers.SlugRelatedField(slug_field="uuid", queryset=DeviceType.objects.all())

    class Meta:
        model = ServiceOrder
        fields = [
            "uuid",
            "document_type_uuid",
            "category_uuid",
            "number_scheme",
            "number",
            "status",
            "state",
            "contractor_uuid",
            "user_uuid",
            "document_date",
            "acceptance_date",
            "realization_date",
            "closing_date",
            "warehouse_uuid",
            "stage_uuid",
            "net_value",
            "gross_value",
            "description",
            "device_uuid",
        ]
