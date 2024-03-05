from django.db.utils import IntegrityError

from config import celery_app
from crm.documents.models import DocumentType
from crm.service.models import (
    Attribute,
    AttributeDefinition,
    AttributeDefinitionItem,
    Category,
    Device,
    DeviceType,
    Note,
    ServiceActivity,
    ServiceOrder,
    ServicePart,
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
    ServiceActivitySerializer,
    ServiceOrderSerializer,
    ServicePartSerializer,
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
    ServiceActivityObject,
    ServiceOrderObject,
    ServicePartObject,
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
    device_object = DeviceObject()
    device_objects = device_object.get()
    for dev_obj in device_objects:
        serializer = DeviceSerializer(dev_obj)
        Device.objects.create(**serializer.data)


@celery_app.task()
def import_service_orders():
    service_order_object = ServiceOrderObject()
    objects = service_order_object.get()
    for obj in objects:
        serializer = ServiceOrderSerializer(obj)
        ServiceOrder.objects.update_or_create(optima_id=serializer.data.get("optima_id"), defaults=serializer.data)


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
def update_attributes_definition():
    for obj in Attribute.objects.all().values_list("attribute_definition", flat=True).distinct():
        print(obj)


@celery_app.task()
def full_import_orders():
    service_order_object = ServiceOrderObject()
    for document in DocumentType.objects.filter(to_import=True):
        order_objects = service_order_object.get(document.optima_id, "2024-01-01")
        for order_obj in order_objects:
            serializer = ServiceOrderSerializer(order_obj)
            service_order, created = ServiceOrder.objects.update_or_create(
                optima_id=serializer.data.get("optima_id"), defaults=serializer.data
            )
            service_part_object = ServicePartObject()
            part_objects = service_part_object.get(service_order.optima_id)
            if part_objects:
                for part_obj in part_objects:
                    serializer = ServicePartSerializer(part_obj)
                    if serializer.data:
                        try:
                            ServicePart.objects.update_or_create(
                                optima_id=serializer.data.get("optima_id"), defaults=serializer.data
                            )
                        except Exception as e:
                            print(e)
                            pass
            attribute_object = AttributeObject()
            attr_objects = attribute_object.get(service_order.optima_id)
            if attr_objects:
                for attr_obj in attr_objects:
                    serializer = AttributeSerializer(attr_obj)
                    try:
                        Attribute.objects.update_or_create(
                            optima_id=serializer.data.get("optima_id"), defaults=serializer.data
                        )
                    except IntegrityError:
                        pass
            service_activity_object = ServiceActivityObject()
            activities_objects = service_activity_object.get(service_order.optima_id)
            if activities_objects:
                for activity_obj in activities_objects:
                    serializer = ServiceActivitySerializer(activity_obj)
                    if serializer.data:
                        try:
                            ServiceActivity.objects.update_or_create(
                                optima_id=serializer.data.get("optima_id"), defaults=serializer.data
                            )
                        except Exception as e:
                            print(e)
                            pass
            note_object = NoteObject()
            note_objects = note_object.get(service_order.optima_id)
            if note_objects:
                for note_obj in note_objects:
                    serializer = NoteSerializer(note_obj)
                    Note.objects.update_or_create(optima_id=serializer.data.get("optima_id"), defaults=serializer.data)
