from config import celery_app
from crm.warehouses.models import Warehouse
from crm.warehouses.optima_api.serializers import WarehouseSerializer
from crm.warehouses.optima_api.views import WarehouseObject


@celery_app.task()
def import_warehouses():
    warehouse_object = WarehouseObject()
    warehouses = warehouse_object.get()
    for obj in warehouses:
        serializer = WarehouseSerializer(obj)
        Warehouse.objects.create(**serializer.data)
