from factory import Faker

from crm.contractors.models import Contractor
from crm.core.tests.factories import OptimaModelFactory


class ContractorFactory(OptimaModelFactory):
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

    class Meta:
        model = Contractor
