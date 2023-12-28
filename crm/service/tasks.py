from config import celery_app
from crm.service.models import Category, Device, DeviceType, ServiceOrder, Stage
from crm.service.optima_api.serializers import (
    CategorySerializer,
    DeviceSerializer,
    DeviceTypeSerializer,
    ServiceOrderSerializer,
    StageSerializer,
)
from crm.service.optima_api.views import (
    CategoryObject,
    DeviceObject,
    DeviceTypeObject,
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
