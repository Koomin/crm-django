from rest_framework import serializers

from crm.documents.models import DocumentType
from crm.warehouses.models import Warehouse


class DocumentTypeSerializer(serializers.ModelSerializer):
    warehouse = serializers.SlugRelatedField(slug_field="uuid", queryset=Warehouse.objects.all(), read_only=False)

    class Meta:
        model = DocumentType
        fields = ["uuid", "symbol", "obj_class", "name", "numbering_scheme", "active", "warehouse"]
