from rest_framework import serializers

from crm.documents.models import DocumentType


class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ["uuid", "symbol", "obj_class", "name", "numbering_scheme", "active", "warehouse"]
