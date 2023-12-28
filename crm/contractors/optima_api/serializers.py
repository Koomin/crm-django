from crm.contractors.models import Contractor
from crm.core.optima import BaseOptimaSerializer


class ContractorSerializer(BaseOptimaSerializer):
    model = Contractor

    def _get_name(self):
        return (self.obj[12] + " " + self.obj[13] + " " + self.obj[14]).strip()

    def _get_home_number(self):
        try:
            _home_number = int(self.obj[9])
        except ValueError:
            return None
        else:
            return _home_number

    def _deserialize(self) -> dict:
        return {
            "optima_id": self.obj[0],
            "code": self.obj[1],
            "postal_code": self.obj[2],
            "tax_number": self.obj[3],
            "phone_number": self.obj[4],
            "country": self.obj[5],
            "city": self.obj[6],
            "street": self.obj[7],
            "street_number": self.obj[8],
            "home_number": self._get_home_number(),
            "post": self.obj[10],
            "state": self.obj[11],
            "name": self._get_name(),
        }
