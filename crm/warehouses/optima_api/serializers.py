from crm.core.optima import BaseOptimaSerializer
from crm.warehouses.models import Warehouse


class WarehouseSerializer(BaseOptimaSerializer):
    model = Warehouse

    def _deserialize(self) -> dict:
        return {
            "optima_id": self.obj[0],
            "type": self.obj[1],
            "symbol": self.obj[2],
            "active": self.obj[3],
            "name": self.obj[4],
            "description": self.obj[5],
            "register": self.obj[6],
        }
