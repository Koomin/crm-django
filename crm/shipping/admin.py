from django.contrib import admin
from django.contrib.admin import ModelAdmin

from crm.shipping.models import Shipping, ShippingAddress, ShippingCompany, ShippingMethod, ShippingStatus, Status


@admin.register(ShippingAddress)
class ShippingAddressAdmin(ModelAdmin):
    pass


@admin.register(Shipping)
class ShippingAdmin(ModelAdmin):
    list_display = ("uuid",)


@admin.register(ShippingStatus)
class ShippingStatusAdmin(ModelAdmin):
    pass


@admin.register(Status)
class StatusAdmin(ModelAdmin):
    pass


@admin.register(ShippingCompany)
class ShippingCompanyAdmin(ModelAdmin):
    pass


@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    pass
