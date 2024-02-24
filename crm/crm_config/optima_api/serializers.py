from crm.core.optima import BaseOptimaSerializer
from crm.crm_config.models import Country, State


class StateSerializer(BaseOptimaSerializer):
    model = State

    @staticmethod
    def _get_country():
        return Country.objects.get(code="PL")

    def _deserialize(self) -> dict:
        return {"optima_id": self.obj[0], "name": self.obj[1], "country": self._get_country()}


class CountrySerializer(BaseOptimaSerializer):
    model = Country

    def _deserialize(self) -> dict:
        return {"optima_id": self.obj[0], "name": self.obj[1], "code": self.obj[2]}
