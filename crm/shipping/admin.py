from django.contrib import admin
from django.contrib.admin import ModelAdmin

from crm.shipping.models import Shipping, ShippingAddress


@admin.register(ShippingAddress)
class ShippingAddressAdmin(ModelAdmin):
    pass


@admin.register(Shipping)
class ShippingAdmin(ModelAdmin):
    pass
