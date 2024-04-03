from django.contrib import admin
from django.contrib.admin import ModelAdmin

from crm.shipping.models import Shipping, ShippingAddress, ShippingStatus, Status


@admin.register(ShippingAddress)
class ShippingAddressAdmin(ModelAdmin):
    pass


@admin.register(Shipping)
class ShippingAdmin(ModelAdmin):
    pass


@admin.register(ShippingStatus)
class ShippingStatusAdmin(ModelAdmin):
    pass


@admin.register(Status)
class StatusAdmin(ModelAdmin):
    pass
