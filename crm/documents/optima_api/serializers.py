from crm.core.optima import BaseOptimaSerializer
from crm.documents.models import DocumentType


class DocumentTypeSerializer(BaseOptimaSerializer):
    model = DocumentType

    def _deserialize(self) -> dict:
        return {
            "optima_id": self.obj[0],
            "obj_class": self.obj[1],
            "symbol": self.obj[2],
            "name": self.obj[3],
            "numbering_scheme": self.obj[4],
            "active": self.obj[5],
        }
