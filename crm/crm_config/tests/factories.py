from factory import Faker

from crm.core.tests.factories import BaseModelFactory
from crm.crm_config.models import GeneralSettings, Log


class GeneralSettingsFactory(BaseModelFactory):
    optima_synchronization = Faker("pybool")
    mailing = Faker("pybool")
    optima_config_database = Faker("pystr")
    optima_general_database = Faker("pystr")

    class Meta:
        model = GeneralSettings


class LogFactory(BaseModelFactory):
    exception_traceback = Faker("pystr")
    method_name = Faker("pystr")
    model_name = Faker("pystr")
    object_uuid = Faker("uuid4")
    object_serialized = Faker("pystr")
    status = Faker("random_int", min=0, max=1)

    class Meta:
        model = Log
