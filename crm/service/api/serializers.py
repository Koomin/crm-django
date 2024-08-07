from rest_framework import serializers

from crm.contractors.models import Contractor
from crm.core.api.fields import FileBase64Field, FileTypeField
from crm.core.api.serializers import OptimaSerializer
from crm.crm_config.api.serializers import EmailTemplateSerializer, ServiceAddressSerializer, TaxPercentageSerializer
from crm.crm_config.models import EmailTemplate, ServiceAddress, TaxPercentage
from crm.documents.models import DocumentType
from crm.products.api.serializers import ProductSerializer
from crm.products.models import Product
from crm.service.models import (
    Attribute,
    AttributeDefinition,
    AttributeDefinitionItem,
    Category,
    Device,
    DeviceCatalog,
    DeviceType,
    EmailSent,
    FormFile,
    Note,
    OrderType,
    ServiceActivity,
    ServiceOrder,
    ServicePart,
    Stage,
    StageDuration,
)
from crm.users.models import OptimaUser, User
from crm.warehouses.models import Warehouse


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["uuid", "code", "code_detailed", "description"]


class StageSerializer(serializers.ModelSerializer):
    email_template = EmailTemplateSerializer(read_only=True)
    attributes = serializers.SlugRelatedField(
        slug_field="uuid", queryset=AttributeDefinition.objects.all(), read_only=False, many=True
    )

    class Meta:
        model = Stage
        fields = ["uuid", "type", "code", "description", "email_template", "attributes"]


class StageUpdateSerializer(serializers.ModelSerializer):
    email_template = serializers.SlugRelatedField(
        slug_field="uuid", queryset=EmailTemplate.objects.all(), read_only=False
    )
    attributes = serializers.SlugRelatedField(
        slug_field="uuid", queryset=AttributeDefinition.objects.all(), read_only=False, many=True
    )

    class Meta:
        model = Stage
        fields = ["uuid", "type", "code", "description", "email_template", "attributes"]


class DeviceCatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceCatalog
        fields = ["uuid", "name", "active"]


class DeviceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = ["uuid", "code", "active", "name"]


class DeviceSerializer(serializers.ModelSerializer):
    from crm.shipping.models import ShippingCompany, ShippingMethod

    device_type = serializers.SlugRelatedField(slug_field="uuid", read_only=True)
    document_type = serializers.SlugRelatedField(
        slug_field="uuid", queryset=DocumentType.objects.all(), read_only=False
    )
    # shipping_company = serializers.SlugRelatedField(
    #     slug_field="uuid", queryset=ShippingCompany.objects.all(), read_only=False
    # )
    shipping_method = serializers.SlugRelatedField(
        slug_field="uuid", queryset=ShippingMethod.objects.all(), many=True, read_only=False
    )
    device_catalog = serializers.SlugRelatedField(
        slug_field="uuid", queryset=DeviceCatalog.objects.all(), read_only=False
    )
    available_services = serializers.SlugRelatedField(slug_field="uuid", many=True, read_only=True)

    class Meta:
        model = Device
        fields = [
            "uuid",
            "code",
            "name",
            "description",
            "device_type",
            "document_type",
            # "shipping_company",
            "device_catalog",
            "shipping_method",
            "available_services",
        ]


class NoteSerializer(OptimaSerializer):
    service_order = serializers.SlugRelatedField(
        slug_field="uuid", queryset=ServiceOrder.objects.all(), read_only=False
    )

    class Meta:
        model = Note
        fields = ["uuid", "service_order", "number", "date", "description", "user"]


class FormFileSerializer(serializers.ModelSerializer):
    file = FileBase64Field()

    class Meta:
        model = FormFile
        fields = ["file"]


class ServiceActivitySerializer(OptimaSerializer):
    product = serializers.SlugRelatedField(slug_field="uuid", queryset=Product.objects.all(), read_only=False)
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_code = serializers.CharField(source="product.code", read_only=True)
    user_code = serializers.CharField(source="user.code", read_only=True)
    user = serializers.SlugRelatedField(slug_field="uuid", queryset=OptimaUser.objects.all(), read_only=False)
    service_order = serializers.SlugRelatedField(
        slug_field="uuid", queryset=ServiceOrder.objects.all(), read_only=False
    )
    date_from = serializers.DateTimeField(format="%Y-%m-%d", required=False)
    date_to = serializers.DateTimeField(format="%Y-%m-%d", required=False)
    tax_percentage = serializers.SlugRelatedField(
        slug_field="uuid", queryset=TaxPercentage.objects.all(), read_only=False
    )

    class Meta:
        model = ServiceActivity
        fields = [
            "uuid",
            "number",
            "product",
            "product_name",
            "product_code",
            "to_invoicing",
            "user_code",
            "user",
            "is_finished",
            "date_of_service",
            "date_from",
            "date_to",
            "price_net",
            "price_gross",
            "price_discount",
            "quantity",
            "value_net",
            "value_gross",
            "unit",
            "service_order",
            "tax_percentage",
            "service_cost",
        ]


class ServiceActivityReadSerializer(OptimaSerializer):
    product = ProductSerializer()
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_code = serializers.CharField(source="product.code", read_only=True)
    user_code = serializers.CharField(source="user.code", read_only=True)
    user = serializers.SlugRelatedField(slug_field="uuid", queryset=OptimaUser.objects.all(), read_only=False)
    service_order = serializers.SlugRelatedField(
        slug_field="uuid", queryset=ServiceOrder.objects.all(), read_only=False
    )
    date_from = serializers.DateTimeField(format="%Y-%m-%d", required=False)
    date_to = serializers.DateTimeField(format="%Y-%m-%d", required=False)
    tax_percentage = TaxPercentageSerializer()

    class Meta:
        model = ServiceActivity
        fields = [
            "uuid",
            "number",
            "product",
            "product_name",
            "product_code",
            "to_invoicing",
            "user_code",
            "user",
            "is_finished",
            "date_of_service",
            "date_from",
            "date_to",
            "price_net",
            "price_gross",
            "price_discount",
            "quantity",
            "value_net",
            "value_gross",
            "unit",
            "service_order",
            "tax_percentage",
            "service_cost",
        ]


class ServicePartSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_code = serializers.CharField(source="product.code", read_only=True)
    warehouse = serializers.CharField(source="warehouse.symbol", read_only=True)
    user = serializers.CharField(source="user.code", read_only=True)

    class Meta:
        model = ServicePart
        fields = [
            "uuid",
            "number",
            "product",
            "product_name",
            "product_code",
            "to_invoicing",
            "user",
            "warehouse",
            "price_net",
            "price_gross",
            "price_discount",
            "quantity",
            "quantity_collected",
            "quantity_released",
            "status_collected",
            "unit",
            "to_return",
            "document",
        ]


class ServiceOrderSerializer(OptimaSerializer):
    document_type = serializers.SlugRelatedField(
        slug_field="uuid", queryset=DocumentType.objects.all(), read_only=False
    )
    order_type = serializers.SlugRelatedField(slug_field="uuid", queryset=OrderType.objects.all(), read_only=False)
    order_type_name = serializers.CharField(source="order_type.name", allow_null=True, required=False)
    document_type_name = serializers.CharField(source="document_type.symbol", allow_null=True, required=False)
    category = serializers.SlugRelatedField(slug_field="uuid", queryset=Category.objects.all(), read_only=False)
    category_code = serializers.CharField(source="category.code", allow_null=True, required=False)
    contractor = serializers.SlugRelatedField(slug_field="uuid", queryset=Contractor.objects.all(), read_only=False)
    contractor_ext_id = serializers.IntegerField(source="contractor.optima_id", read_only=True, required=False)
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
    form_files = FormFileSerializer(many=True, read_only=True)
    purchase_document_type = FileTypeField(source="purchase_document", required=False, read_only=True)
    contractor_confirmed = serializers.BooleanField(source="contractor.confirmed", read_only=True)
    service_parts = ServicePartSerializer(many=True, read_only=True)
    service_activities = ServiceActivitySerializer(many=True, read_only=True)
    service_address = ServiceAddressSerializer(read_only=True)

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
            "in_buffer",
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
            "form_files",
            "service_parts",
            "service_activities",
            "service_address",
            "contractor_ext_id",
        ]


class OrderTypeSerializer(serializers.ModelSerializer):
    warehouse = serializers.SlugRelatedField(slug_field="uuid", queryset=Warehouse.objects.all(), read_only=False)

    class Meta:
        model = OrderType
        fields = ["uuid", "name", "warehouse"]


class PurchaseDocumentSerializer(serializers.ModelSerializer):
    purchase_document_base64 = FileBase64Field(source="purchase_document")
    service_order_uuid = serializers.UUIDField(source="uuid")

    class Meta:
        model = ServiceOrder
        fields = ["service_order_uuid", "purchase_document", "purchase_document_number", "purchase_document_base64"]


class NewServiceOrderSerializer(serializers.ModelSerializer):
    contractor = serializers.SlugRelatedField(slug_field="uuid", queryset=Contractor.objects.all(), read_only=False)
    order_type = serializers.SlugRelatedField(slug_field="uuid", queryset=OrderType.objects.all(), read_only=False)
    form_files = FormFileSerializer(many=True, read_only=True)
    device = serializers.SlugRelatedField(slug_field="uuid", queryset=Device.objects.all(), read_only=False)
    service_address = serializers.SlugRelatedField(
        slug_field="uuid", queryset=ServiceAddress.objects.all(), read_only=False, required=False
    )

    class Meta:
        model = ServiceOrder
        fields = [
            "contractor",
            "contractor_name",
            "contractor_name1",
            "contractor_name2",
            "contractor_name3",
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
            "purchase_date",
            "document_date",
            "acceptance_date",
            "form_files",
            "device",
            "service_address",
            "category",
        ]

    def create(self, validated_data):
        form_files = []
        if self.initial_data.get("form_files"):
            form_files = self.initial_data.pop("form_files")
        new_service_order = ServiceOrder.objects.create(**validated_data)
        for form_file in form_files:
            FormFile.objects.create(service_order=new_service_order, file=form_file)
        return new_service_order


class AttributeSerializer(OptimaSerializer):
    service_order = serializers.SlugRelatedField(
        slug_field="uuid", queryset=ServiceOrder.objects.all(), read_only=False
    )
    attribute_definition = serializers.SlugRelatedField(
        slug_field="uuid", queryset=AttributeDefinition.objects.all(), read_only=False
    )
    attribute_definition_type = serializers.IntegerField(source="attribute_definition.type", read_only=True)
    attribute_definition_format = serializers.IntegerField(source="attribute_definition.format", read_only=True)
    attribute_definition_code = serializers.CharField(source="attribute_definition.code", read_only=True)

    class Meta:
        model = Attribute
        fields = [
            "uuid",
            "code",
            "value",
            "service_order",
            "attribute_definition",
            "attribute_definition_type",
            "attribute_definition_format",
            "attribute_definition_code",
        ]


class AttributeDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeDefinition
        fields = ["uuid", "code", "type", "format", "is_active"]


class AttributeDefinitionItemSerializer(serializers.ModelSerializer):
    attribute_definition = serializers.SlugRelatedField(
        slug_field="uuid", queryset=AttributeDefinition.objects.all(), read_only=False
    )

    class Meta:
        model = AttributeDefinitionItem
        fields = ["uuid", "value", "number", "attribute_definition"]


class StageDurationSerializer(serializers.ModelSerializer):
    stage_code = serializers.CharField(source="stage.code", read_only=True)
    service_order = serializers.SlugRelatedField(
        slug_field="uuid", queryset=ServiceOrder.objects.all(), read_only=False
    )
    stage = serializers.SlugRelatedField(slug_field="uuid", queryset=Stage.objects.all(), read_only=False)
    start_date = serializers.DateTimeField(source="start", format="%Y-%m-%d", required=False)
    start_time = serializers.DateTimeField(source="start", format="%H:%M:%S", required=False)
    end_date = serializers.DateTimeField(source="end", format="%Y-%m-%d", required=False)
    end_time = serializers.DateTimeField(source="end", format="%H:%M:%S", required=False)

    class Meta:
        model = StageDuration
        fields = [
            "uuid",
            "start",
            "start_date",
            "start_time",
            "end",
            "end_date",
            "end_time",
            "stage",
            "stage_code",
            "service_order",
        ]


class EmailSentSerializer(serializers.ModelSerializer):
    stage = serializers.CharField(source="stage.code", read_only=True)
    service_order = serializers.CharField(source="service_order.full_number", read_only=True)

    class Meta:
        model = EmailSent
        fields = [
            "uuid",
            "stage",
            "subject",
            "message",
            "date_of_sent",
            "service_order",
            "sent",
            "email",
        ]
