from django.contrib import admin
from django.contrib.admin import ModelAdmin

from crm.warehouses.models import Warehouse


@admin.register(Warehouse)
class WarehouseAdmin(ModelAdmin):
    search_fields = ["symbol", "name"]
