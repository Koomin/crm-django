from crm.core.optima import BaseOptimaSerializer
from crm.products.models import Product


class ProductSerializer(BaseOptimaSerializer):
    model = Product

    def _deserialize(self) -> dict:
        return {
            "optima_id": self.obj[0],
            "code": self.obj[1],
            "name": self.obj[2],
            "unit": self.obj[3],
            "type": self.obj[4],
            "price_number": self.obj[5],
        }
