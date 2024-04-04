import pytest

from crm.contractors.tests.factories import ContractorFactory
from crm.users.models import User
from crm.users.tests.factories import OptimaUserFactory, UserFactory
from crm.warehouses.tests.factories import WarehouseFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user(db) -> User:
    return UserFactory()


@pytest.fixture
def optima_user(db):
    return OptimaUserFactory()


@pytest.fixture
def warehouse(db):
    return WarehouseFactory()


@pytest.fixture
def contractor(db):
    return ContractorFactory()
