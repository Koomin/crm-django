from factory import Faker
from factory.django import DjangoModelFactory

from crm.warehouses.models import Warehouse


class WarehouseFactory(DjangoModelFactory):
    uuid = Faker("uuid4")
    optima_id = Faker("random_number")
    type = Faker("random_int", min=1, max=4)
    name = Faker("name")
    description = Faker("pystr", max_chars=50)
    exported = Faker("pybool")
    active = Faker("pybool")
    register = Faker("pystr", max_chars=20)
    symbol = Faker("pystr", max_chars=20)
    created = Faker("date_time_this_year")
    modified = Faker("date_time_this_year")

    class Meta:
        model = Warehouse
