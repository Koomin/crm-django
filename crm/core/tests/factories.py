from factory import Faker, Sequence
from factory.django import DjangoModelFactory


class BaseModelFactory(DjangoModelFactory):
    uuid = Faker("uuid4")
    created = Faker("date_time_this_year")
    modified = Faker("date_time_this_year")


class OptimaModelFactory(BaseModelFactory):
    optima_id = Sequence(lambda n: "%09d" % n)
    exported = Faker("pybool")
