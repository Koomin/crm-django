from config import celery_app
from crm.contractors.models import Contractor
from crm.contractors.optima_api.serializers import ContractorSerializer
from crm.contractors.optima_api.views import ContractorObject


@celery_app.task()
def import_contractors():
    contractor_object = ContractorObject()
    contractors = contractor_object.get()
    for obj in contractors:
        serializer = ContractorSerializer(obj)
        if serializer.data:
            Contractor.objects.update_or_create(optima_id=serializer.data.get("optima_id"), defaults=serializer.data)
