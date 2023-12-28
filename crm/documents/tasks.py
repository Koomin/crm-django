from config import celery_app
from crm.documents.models import DocumentType
from crm.documents.optima_api.serializers import DocumentTypeSerializer
from crm.documents.optima_api.views import DocumentTypeObject


@celery_app.task()
def import_document_types():
    document_type_object = DocumentTypeObject()
    document_types = document_type_object.get()
    for obj in document_types:
        serializer = DocumentTypeSerializer(obj)
        DocumentType.objects.create(**serializer.data)
