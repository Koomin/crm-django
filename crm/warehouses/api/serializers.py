from rest_framework import serializers

from crm.warehouses.models import Warehouse


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ["uuid", "type", "name", "description", "symbol", "register", "active"]
