from django.db.utils import IntegrityError

from config import celery_app
from crm.service.models import (
    Attribute,
    AttributeDefinition,
    AttributeDefinitionItem,
    Category,
    Device,
    DeviceType,
    Note,
    ServiceOrder,
    Stage,
)
from crm.service.optima_api.serializers import (
    AttributeDefinitionItemSerializer,
    AttributeDefinitionSerializer,
    AttributeSerializer,
    CategorySerializer,
    DeviceSerializer,
    DeviceTypeSerializer,
    NoteSerializer,
    ServiceOrderSerializer,
    StageSerializer,
)
from crm.service.optima_api.views import (
    AttributeDefinitionItemObject,
    AttributeDefinitionObject,
    AttributeObject,
    CategoryObject,
    DeviceObject,
    DeviceTypeObject,
    NoteObject,
    ServiceOrderObject,
    StageObject,
)


@celery_app.task()
def import_categories():
    category_object = CategoryObject()
    objects = category_object.get()
    for obj in objects:
        serializer = CategorySerializer(obj)
        Category.objects.create(**serializer.data)


@celery_app.task()
def import_stages():
    stage_object = StageObject()
    objects = stage_object.get()
    for obj in objects:
        serializer = StageSerializer(obj)
        Stage.objects.create(**serializer.data)


@celery_app.task()
def import_device_types():
    device_type_object = DeviceTypeObject()
    objects = device_type_object.get()
    for obj in objects:
        serializer = DeviceTypeSerializer(obj)
        DeviceType.objects.create(**serializer.data)


@celery_app.task()
def import_devices():
    device_object = DeviceObject()
    objects = device_object.get()
    for obj in objects:
        serializer = DeviceSerializer(obj)
        Device.objects.create(**serializer.data)


@celery_app.task()
def import_service_orders():
    service_order_object = ServiceOrderObject()
    objects = service_order_object.get()
    for obj in objects:
        serializer = ServiceOrderSerializer(obj)
        ServiceOrder.objects.update_or_create(optima_id=serializer.data.get("optima_id"), defaults=serializer.data)


@celery_app.task()
def import_notes():
    note_object = NoteObject()
    objects = note_object.get()
    for obj in objects:
        serializer = NoteSerializer(obj)
        Note.objects.update_or_create(optima_id=serializer.data.get("optima_id"), defaults=serializer.data)


@celery_app.task()
def import_attributes_definition():
    attribute_object = AttributeDefinitionObject()
    objects = attribute_object.get()
    for obj in objects:
        serializer = AttributeDefinitionSerializer(obj)
        AttributeDefinition.objects.update_or_create(
            optima_id=serializer.data.get("optima_id"), defaults=serializer.data
        )
    attribute_item_object = AttributeDefinitionItemObject()
    objects = attribute_item_object.get()
    for obj in objects:
        serializer = AttributeDefinitionItemSerializer(obj)
        try:
            AttributeDefinitionItem.objects.update_or_create(
                optima_id=serializer.data.get("optima_id"), defaults=serializer.data
            )
        except IntegrityError:
            pass


@celery_app.task()
def import_attributes():
    orders = ServiceOrder.objects.filter(optima_id__isnull=False)
    for order in orders:
        attribute_object = AttributeObject()
        objects = attribute_object.get(order.optima_id)
        if objects:
            for obj in objects:
                serializer = AttributeSerializer(obj)
                try:
                    Attribute.objects.update_or_create(
                        optima_id=serializer.data.get("optima_id"), defaults=serializer.data
                    )
                except IntegrityError:
                    pass


@celery_app.task()
def update_attributes_definition():
    for obj in Attribute.objects.all().values_list("attribute_definition", flat=True).distinct():
        print(obj)
