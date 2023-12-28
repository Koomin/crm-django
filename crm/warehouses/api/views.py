from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from crm.core.api.views import BaseViewSet
from crm.warehouses.api.serializers import WarehouseSerializer
from crm.warehouses.models import Warehouse


class WarehouseViewSet(ListModelMixin, RetrieveModelMixin, BaseViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
