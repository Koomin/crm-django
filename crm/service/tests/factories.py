from factory import Faker, SubFactory

from crm.contractors.tests.factories import ContractorFactory
from crm.core.tests.factories import BaseModelFactory, OptimaModelFactory
from crm.crm_config.tests.factories import EmailTemplateFactory, TaxPercentageFactory
from crm.documents.tests.factories import DocumentTypeFactory
from crm.products.tests.factories import ProductFactory
from crm.service.models import Category, Device, DeviceType, OrderType, ServiceActivity, ServiceOrder, Stage
from crm.users.tests.factories import OptimaUserFactory, UserFactory
from crm.warehouses.tests.factories import WarehouseFactory


class StageFactory(OptimaModelFactory):
    type = Faker("random_number")
    code = Faker("pystr", max_chars=50)
    description = Faker("pystr", max_chars=255)
    email_template = SubFactory(EmailTemplateFactory)
    is_default = Faker("pybool")

    class Meta:
        model = Stage


class OrderTypeFactory(BaseModelFactory):
    name = Faker("pystr", max_chars=50)

    class Meta:
        model = OrderType


class CategoryFactory(OptimaModelFactory):
    code = Faker("pystr", max_chars=255)
    code_detailed = Faker("pystr", max_chars=255)
    description = Faker("pystr", max_chars=1024)

    class Meta:
        model = Category


class DeviceTypeFactory(OptimaModelFactory):
    code = Faker("pystr", max_chars=255)
    active = Faker("pybool")
    name = Faker("pystr", max_chars=255)

    class Meta:
        model = DeviceType


class DeviceFactory(OptimaModelFactory):
    code = Faker("pystr", max_chars=255)
    name = Faker("pystr", max_chars=255)
    description = Faker("pystr", max_chars=1024)
    device_type = SubFactory(DeviceTypeFactory)
    document_type = SubFactory(DocumentTypeFactory)

    class Meta:
        model = Device


class ServiceOrderFactory(OptimaModelFactory):
    document_type = SubFactory(DocumentTypeFactory)
    category = SubFactory(CategoryFactory)
    number_scheme = Faker("pystr", max_chars=255)
    number = Faker("random_number")
    full_number = Faker("pystr", max_chars=255)
    in_buffer = Faker("pybool")
    state = Faker("random_element", elements=[0, 1, 2, 3, 99])
    contractor = SubFactory(ContractorFactory)
    contractor_type = Faker("random_number")
    contractor_name = Faker("pystr", max_chars=1024)
    contractor_name1 = Faker("pystr", max_chars=1024)
    contractor_name2 = Faker("pystr", max_chars=1024)
    contractor_name3 = Faker("pystr", max_chars=1024)
    contractor_city = Faker("city")
    contractor_country = Faker("country")
    contractor_street = Faker("street_name")
    contractor_street_number = Faker("building_number")
    contractor_home_number = Faker("building_number")
    contractor_state = Faker("pystr", max_chars=40)
    contractor_post = Faker("city")
    contractor_postal_code = Faker("postcode")
    user = SubFactory(UserFactory)
    document_date = Faker("date_time_this_year")
    acceptance_date = Faker("date_time_this_year")
    realization_date = Faker("date_time_this_year")
    closing_date = Faker("date_time_this_year")
    warehouse = SubFactory(WarehouseFactory)
    stage = SubFactory(StageFactory)
    net_value = Faker("pydecimal", left_digits=8, right_digits=2)
    gross_value = Faker("pydecimal", left_digits=8, right_digits=2)
    description = Faker("paragraph")
    device = SubFactory(DeviceFactory)
    serial_number = Faker("pystr", max_chars=255)
    purchase_document_number = Faker("pystr", max_chars=255)
    purchase_date = Faker("date_this_year")
    email = Faker("email")
    phone_number = Faker("phone_number")
    order_type = SubFactory(OrderTypeFactory)

    class Meta:
        model = ServiceOrder


class ServiceActivityFactory(OptimaModelFactory):
    service_order = SubFactory(ServiceOrderFactory)
    number = Faker("random_number")
    product = SubFactory(ProductFactory)
    user = SubFactory(OptimaUserFactory)
    is_finished = Faker("pybool")
    to_invoicing = Faker("pybool")
    date_of_service = Faker("date_time_this_year")
    date_from = Faker("date_time_this_year")
    date_to = Faker("date_time_this_year")
    price_net = Faker("pydecimal", left_digits=8, right_digits=2)
    price_gross = Faker("pydecimal", left_digits=10, right_digits=2)
    price_discount = Faker("pydecimal", left_digits=8, right_digits=2)
    service_cost = Faker("pydecimal", left_digits=8, right_digits=2)
    value_net = Faker("pydecimal", left_digits=18, right_digits=2)
    value_gross = Faker("pydecimal", left_digits=18, right_digits=2)
    tax_percentage = SubFactory(TaxPercentageFactory)
    quantity = Faker("pydecimal", left_digits=4, right_digits=2)
    unit = Faker("pystr", max_chars=10)

    class Meta:
        model = ServiceActivity
