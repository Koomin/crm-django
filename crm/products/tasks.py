from config import celery_app
from crm.products.optima_api.serializers import ProductSerializer
from crm.products.optima_api.views import ProductObject


@celery_app.task()
def import_products():
    product_object = ProductObject()
    objects = product_object.get()
    for obj in objects:
        serializer = ProductSerializer(obj)
        serializer.model.objects.update_or_create(optima_id=serializer.data.get("optima_id"), defaults=serializer.data)
