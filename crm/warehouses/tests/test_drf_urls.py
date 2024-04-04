from django.urls import resolve, reverse

from crm.warehouses.models import Warehouse


def test_warehouse_detail(warehouse: Warehouse):
    assert reverse("api:warehouse-detail", kwargs={"uuid": warehouse.uuid}) == f"/api/v1/warehouses/{warehouse.uuid}/"
    assert resolve(f"/api/v1/warehouses/{warehouse.uuid}/").view_name == "api:warehouse-detail"


def test_warehouse_list():
    assert reverse("api:warehouse-list") == "/api/v1/warehouses/"
    assert resolve("/api/v1/warehouses/").view_name == "api:warehouse-list"
