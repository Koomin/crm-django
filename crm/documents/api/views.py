from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from crm.core.api.views import BaseViewSet
from crm.documents.api.serializers import DocumentTypeSerializer
from crm.documents.models import DocumentType


class DocumentTypeViewSet(ListModelMixin, RetrieveModelMixin, BaseViewSet):
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer
