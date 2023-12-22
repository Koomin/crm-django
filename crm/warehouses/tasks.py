from config import celery_app
from crm.warehouses.models import Warehouse


@celery_app.task()
def import_warehouses():
    warehouse_object = WarehouseObject()
    warehouses = warehouse_object.get()
    for obj in warehouses:
        serializer = WarehouseSerializer(obj)
        Warehouse.objects.create(**serializer)

