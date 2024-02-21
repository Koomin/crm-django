from rest_framework import serializers

from crm.contractors.models import Contractor
from crm.core.api.fields import FileBase64Field, FileTypeField
from crm.documents.models import DocumentType
from crm.service.models import Category, Device, DeviceType, Note, OrderType, ServiceOrder, Stage
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
    device_type = serializers.SlugRelatedField(slug_field="uuid", read_only=True)
    document_type = serializers.SlugRelatedField(
        slug_field="uuid", queryset=DocumentType.objects.all(), read_only=False
    )

    class Meta:
        model = Device
        fields = ["uuid", "code", "name", "description", "device_type", "document_type"]


class NoteSerializer(serializers.ModelSerializer):
    service_order = serializers.SlugRelatedField(
        slug_field="uuid", queryset=ServiceOrder.objects.all(), read_only=False
    )

    class Meta:
        model = Note
        fields = ["uuid", "service_order", "number", "date", "description", "user"]


class ServiceOrderSerializer(serializers.ModelSerializer):
    document_type = serializers.SlugRelatedField(
        slug_field="uuid", queryset=DocumentType.objects.all(), read_only=False
    )
    order_type = serializers.SlugRelatedField(slug_field="uuid", queryset=OrderType.objects.all(), read_only=False)
    order_type_name = serializers.CharField(source="order_type.name", allow_null=True, required=False)
    document_type_name = serializers.CharField(source="document_type.symbol", allow_null=True, required=False)
    category = serializers.SlugRelatedField(slug_field="uuid", queryset=Category.objects.all(), read_only=False)
    category_code = serializers.CharField(source="category.code", allow_null=True, required=False)
    contractor = serializers.SlugRelatedField(slug_field="uuid", queryset=Contractor.objects.all(), read_only=False)
    # contractor_name = serializers.CharField(source="contractor.name", allow_null=True, required=False)
    user = serializers.SlugRelatedField(slug_field="uuid", queryset=User.objects.all(), read_only=False)
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
    purchase_document_base64 = FileBase64Field(source="purchase_document", required=False, read_only=True)
    purchase_document_type = FileTypeField(source="purchase_document", required=False, read_only=True)
    contractor_confirmed = serializers.BooleanField(source="contractor.confirmed", read_only=True)

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
            "contractor_city",
            "contractor_country",
            "contractor_street",
            "contractor_street_number",
            "contractor_home_number",
            "contractor_state",
            "contractor_post",
            "contractor_postal_code",
            "contractor_confirmed",
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
            "serial_number",
            "purchase_document_number",
            "purchase_document",
            "purchase_date",
            "order_type",
            "order_type_name",
            "email",
            "phone_number",
            "purchase_document_base64",
            "purchase_document_type",
        ]


class OrderTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderType
        fields = ["uuid", "name"]


class PurchaseDocumentSerializer(serializers.ModelSerializer):
    purchase_document_base64 = FileBase64Field(source="purchase_document")
    service_order_uuid = serializers.UUIDField(source="uuid")

    class Meta:
        model = ServiceOrder
        fields = ["serivce_order_uuid", "purchase_document", "purchase_document_number", "purchase_document_base64"]


class NewServiceOrderSerializer(serializers.ModelSerializer):
    contractor = serializers.SlugRelatedField(slug_field="uuid", queryset=Contractor.objects.all(), read_only=False)
    order_type = serializers.SlugRelatedField(slug_field="uuid", queryset=OrderType.objects.all(), read_only=False)

    class Meta:
        model = ServiceOrder
        fields = [
            "contractor",
            "contractor_name",
            "contractor_city",
            "contractor_country",
            "contractor_street",
            "contractor_postal_code",
            "contractor_street_number",
            "contractor_home_number",
            "contractor_state",
            "description",
            "email",
            "phone_number",
            "purchase_document_number",
            "serial_number",
            "order_type",
            "purchase_document",
        ]
