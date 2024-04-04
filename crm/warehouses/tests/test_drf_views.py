import pytest
from rest_framework.test import APIRequestFactory

from crm.users.models import User
from crm.warehouses.api.views import WarehouseViewSet
from crm.warehouses.models import Warehouse


class TestWarehouseViewSet:
    @pytest.fixture
    def api_rf(self) -> APIRequestFactory:
        return APIRequestFactory()

    def test_get_queryset(self, user: User, warehouse: Warehouse, api_rf: APIRequestFactory):
        view = WarehouseViewSet()
        request = api_rf.get("/fake-url/")
        request.user = user
        view.request = request

        assert warehouse in view.get_queryset()

    def test_retrieve_all_warehouses(self, user: User, warehouse: Warehouse, api_rf: APIRequestFactory):
        view = WarehouseViewSet()
        request = api_rf.get("/fake-url/")
        request.user = user
        view.request = request

        queryset = view.get_queryset()

        assert len(queryset) == Warehouse.objects.count()
        assert all(isinstance(obj, Warehouse) for obj in queryset)
