from factory import Faker, SubFactory

from crm.core.tests.factories import OptimaModelFactory
from crm.documents.models import DocumentType
from crm.warehouses.tests.factories import WarehouseFactory


class DocumentTypeFactory(OptimaModelFactory):
    symbol = Faker("pystr", max_chars=12)
    obj_class = Faker("random_number")
    name = Faker("pystr", max_chars=255)
    numbering_scheme = Faker("pystr", max_chars=500)
    active = Faker("pybool")
    warehouse = SubFactory(WarehouseFactory)
    to_import = Faker("pybool")

    class Meta:
        model = DocumentType
