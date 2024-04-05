from factory import Faker
from factory.django import DjangoModelFactory


class BaseModelFactory(DjangoModelFactory):
    uuid = Faker("uuid4")
    created = Faker("date_time_this_year")
    modified = Faker("date_time_this_year")


class OptimaModelFactory(BaseModelFactory):
    optima_id = Faker("random_number")
    exported = Faker("pybool")
