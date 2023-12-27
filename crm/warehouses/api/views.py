from rest_framework import mixins

from crm.core.api.views import BaseViewSet
from crm.warehouses.api.serializers import WarehouseSerializer
from crm.warehouses.models import Warehouse


class WarehouseViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, BaseViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
