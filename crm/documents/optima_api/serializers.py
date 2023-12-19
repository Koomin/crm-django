from crm.core.optima import BaseOptimaSerializer
from crm.documents.models import DocumentType


class DocumentTypeSerializer(BaseOptimaSerializer):
    model = DocumentType

    def _deserialize(self) -> dict:
        return {}
