from factory import Faker

from crm.core.tests.factories import BaseModelFactory
from crm.crm_config.models import EmailTemplate, GeneralSettings, Log, TaxPercentage


class GeneralSettingsFactory(BaseModelFactory):
    optima_synchronization = Faker("pybool")
    mailing = Faker("pybool")
    optima_config_database = Faker("pystr", max_chars=255)
    optima_general_database = Faker("pystr", max_chars=255)

    class Meta:
        model = GeneralSettings


class LogFactory(BaseModelFactory):
    exception_traceback = Faker("pystr")
    method_name = Faker("pystr", max_chars=255)
    model_name = Faker("pystr", max_chars=255)
    object_uuid = Faker("uuid4")
    object_serialized = Faker("pystr")
    status = Faker("random_int", min=0, max=1)

    class Meta:
        model = Log


class EmailTemplateFactory(BaseModelFactory):
    name = Faker("pystr", max_chars=255)
    template = Faker("sentence")
    subject = Faker("pystr", max_chars=255)

    class Meta:
        model = EmailTemplate


class TaxPercentageFactory(BaseModelFactory):
    name = Faker("pystr", max_chars=12)
    value = Faker("pydecimal", left_digits=2, right_digits=2)

    class Meta:
        model = TaxPercentage
