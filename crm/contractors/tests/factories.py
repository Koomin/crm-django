from factory import Faker
from factory.django import DjangoModelFactory

from crm.contractors.models import Contractor


class ContractorFactory(DjangoModelFactory):
    uuid = Faker("uuid4")
    optima_id = Faker("random_number")
    code = Faker("pystr", max_chars=120)
    postal_code = Faker("pystr", max_chars=20)
    tax_number = Faker("random_number")
    phone_number = Faker("phone_number")
    country = Faker("country")
    city = Faker("city")
    street = Faker("street_address")
    home_number = Faker("building_number")
    post = Faker("city")
    state = Faker("pystr")
    name = Faker("company")
    confirmed = Faker("pybool")
    exported = Faker("pybool")
    created = Faker("date_time_this_year")
    modified = Faker("date_time_this_year")

    class Meta:
        model = Contractor
