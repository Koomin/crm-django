from factory import Faker

from crm.core.tests.factories import OptimaModelFactory
from crm.products.models import Product


class ProductFactory(OptimaModelFactory):
    name = Faker("pystr", max_chars=255)
    code = Faker("pystr", max_chars=50)
    unit = Faker("pystr", max_chars=10)
    type = Faker("random_int", min=0, max=1)
    price_number = Faker("random_int")

    class Meta:
        model = Product
