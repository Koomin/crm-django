from django.contrib import admin

from crm.service.models import Attribute, AttributeDefinition
from crm.shipping.models import ShippingMethod


@admin.action(description="Set active")
def set_active(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description="Set inactive")
def set_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)
    for obj in AttributeDefinition.objects.filter(
        pk__in=Attribute.objects.all().values_list("attribute_definition__pk", flat=True).distinct()
    ):
        obj.is_active = True
        obj.save()


@admin.action(description="Set standard package")
def set_standard_package(modeladmin, request, queryset):
    standard_package = ShippingMethod.objects.get(name="Przesyłka standardowa")
    for obj in queryset:
        for device in obj.devices.all():
            device.shipping_method.set([standard_package])
