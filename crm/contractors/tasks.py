from config import celery_app
from crm.contractors.models import Contractor
from crm.contractors.optima_api.serializers import ContractorAttributeSerializer, ContractorSerializer
from crm.contractors.optima_api.views import ContractorAttributeObject, ContractorObject
from crm.crm_config.models import Log


@celery_app.task()
def import_contractors():
    contractor_object = ContractorObject()
    contractors = contractor_object.get()
    for obj in contractors:
        serializer = ContractorSerializer(obj)
        if serializer.data:
            Contractor.objects.update_or_create(optima_id=serializer.data.get("optima_id"), defaults=serializer.data)


@celery_app.task()
def create_attributes(contractor_pk):
    try:
        contractor = Contractor.objects.get(pk=contractor_pk)
    except Exception as e:
        Log.objects.create(
            exception_traceback=e,
            method_name="create_attributes",
            model_name="Contractor",
            object_serialized=f"contractor_pk: {contractor_pk}",
        )
        return
    for code in [116, 118]:
        serializer = ContractorAttributeSerializer(contractor, code)
        if serializer.is_valid():
            attr_connection = ContractorAttributeObject()
            created, _ = attr_connection.post(serializer.data)
    return
