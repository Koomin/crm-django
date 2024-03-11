from django.db.utils import IntegrityError

from config import celery_app
from crm.crm_config.models import Log
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
        if serializer.data:
            Category.objects.update_or_create(optima_id=serializer.data.get("optima_id"), defaults=serializer.data)


@celery_app.task()
def import_stages():
    stage_object = StageObject()
    objects = stage_object.get()
    for obj in objects:
        serializer = StageSerializer(obj)
        if serializer.data:
            Stage.objects.update_or_create(optima_id=serializer.data.get("optima_id"), defaults=serializer.data)


@celery_app.task()
def import_device_types():
    device_type_object = DeviceTypeObject()
    objects = device_type_object.get()
    for obj in objects:
        serializer = DeviceTypeSerializer(obj)
        if serializer.data:
            DeviceType.objects.update_or_create(optima_id=serializer.data.get("optima_id"), defaults=serializer.data)
    device_object = DeviceObject()
    device_objects = device_object.get()
    for dev_obj in device_objects:
        serializer = DeviceSerializer(dev_obj)
        if serializer.data:
            Device.objects.update_or_create(optima_id=serializer.data.get("optima_id"), defaults=serializer.data)


@celery_app.task()
def import_attributes_definition():
    attribute_object = AttributeDefinitionObject()
    objects = attribute_object.get()
    for obj in objects:
        serializer = AttributeDefinitionSerializer(obj)
        if serializer.data:
            AttributeDefinition.objects.update_or_create(
                optima_id=serializer.data.get("optima_id"), defaults=serializer.data
            )
    attribute_item_object = AttributeDefinitionItemObject()
    objects = attribute_item_object.get()
    for obj in objects:
        serializer = AttributeDefinitionItemSerializer(obj)
        if serializer.data:
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


def import_service_order_full(order_objects):
    for order_obj in order_objects:
        serializer = ServiceOrderSerializer(order_obj)
        if serializer.data:
            try:
                service_order = ServiceOrder.objects.get(optima_id=serializer.data.get("optima_id"))
                for key, value in serializer.data.items():
                    setattr(service_order, key, value)
                service_order.save(with_optima_update=False)
            except ServiceOrder.DoesNotExist:
                service_order = ServiceOrder(**serializer.data)
                service_order.save(with_optima_update=False)
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
                    if serializer.data:
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
                    if serializer.data:
                        Note.objects.update_or_create(
                            optima_id=serializer.data.get("optima_id"), defaults=serializer.data
                        )


@celery_app.task()
def full_import_orders():
    service_order_object = ServiceOrderObject()
    for document in DocumentType.objects.filter(to_import=True):
        try:
            order_objects = service_order_object.get(document.optima_id, "2024-01-01")
        except Exception as e:
            from crm.documents.api.serializers import DocumentTypeSerializer

            serializer = DocumentTypeSerializer(document)
            if serializer.is_valid():
                data = serializer.data
            else:
                data = f"document_optima_id: {document.optima_id}"
            Log.objects.create(
                exception_traceback=e,
                method_name="full_import_orders",
                model_name="ServiceOrder",
                object_serialized=data,
            )
            continue
        import_service_order_full(order_objects)


@celery_app.task()
def synchronize_order(optima_id):
    service_order_object = ServiceOrderObject()
    try:
        order_objects = service_order_object.get_by_optima_id(optima_id)
    except Exception as e:
        Log.objects.create(
            exception_traceback=e,
            method_name="synchronize_order",
            model_name="ServiceOrder",
            object_serialized=f"optima_id: {optima_id}",
        )
        return
    import_service_order_full(order_objects)
