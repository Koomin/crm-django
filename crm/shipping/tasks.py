from config import celery_app
from crm.crm_config.models import Log
from crm.service.models import Shipping, ShippingStatus, Status
from crm.shipping.utils import GLSTracking


@celery_app.task()
def shipping_tracking():
    for shipping in Shipping.objects.filter(delivered=False, is_sent=True):
        tracking = GLSTracking(shipping)
        if closed_statuses := tracking.last_closed:
            statuses = [status for status in closed_statuses.values()]
            statuses = list(set(statuses))
            if status := len(statuses) == 1:
                try:
                    status_obj = Status.objects.get(code=status)
                except Status.DoesNotExist as e:
                    Log.objects.create(
                        exception_traceback=e,
                        method_name="shipping_tracking",
                        model_name="Task",
                        object_uuid=shipping.uuid,
                        object_serialized=status,
                    )
                else:
                    ShippingStatus.objects.get_or_create(shipping=shipping, status=status_obj)
                    if status == "DELIVERED":
                        shipping.delivered = True
                        shipping.save()
