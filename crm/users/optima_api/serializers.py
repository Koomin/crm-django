from crm.core.optima import BaseOptimaSerializer
from crm.users.models import OptimaUser


class UserOptimaSerializer(BaseOptimaSerializer):
    model = OptimaUser

    def _deserialize(self) -> dict:
        return {
            "optima_id": self.obj[0],
            "name": self.obj[1],
            "code": self.obj[2],
        }
