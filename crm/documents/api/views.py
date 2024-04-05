from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin

from crm.core.api.views import BaseViewSet
from crm.documents.api.serializers import DocumentTypeSerializer
from crm.documents.models import DocumentType


class DocumentTypeViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, BaseViewSet):
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer
