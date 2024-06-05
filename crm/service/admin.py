from django.contrib import admin
from django.contrib.admin import ModelAdmin

from crm.service.actions import set_active, set_inactive
from crm.service.models import (
    Attribute,
    AttributeDefinition,
    AttributeDefinitionItem,
    Category,
    Device,
    DeviceCatalog,
    DeviceType,
    EmailSent,
    FormFile,
    Note,
    OrderType,
    ServiceActivity,
    ServiceOrder,
    ServicePart,
    Stage,
    StageDuration,
)


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    pass


@admin.register(Stage)
class StageAdmin(ModelAdmin):
    pass


@admin.register(DeviceType)
class DeviceTypeAdmin(ModelAdmin):
    pass


@admin.register(DeviceCatalog)
class DeviceCatalogAdmin(ModelAdmin):
    pass


@admin.register(Device)
class DeviceAdmin(ModelAdmin):
    pass


@admin.register(ServiceOrder)
class ServiceOrder(ModelAdmin):
    pass


@admin.register(Note)
class NoteAdmin(ModelAdmin):
    pass


@admin.register(OrderType)
class OrderTypeAdmin(ModelAdmin):
    pass


@admin.register(Attribute)
class AttributeAdmin(ModelAdmin):
    pass


@admin.register(AttributeDefinitionItem)
class AttributeDefinitionItemAdmin(ModelAdmin):
    pass


@admin.register(AttributeDefinition)
class AttributeDefinitionAdmin(ModelAdmin):
    actions = (set_active, set_inactive)


@admin.register(StageDuration)
class StageDuration(ModelAdmin):
    pass


@admin.register(FormFile)
class FormFileAdmin(ModelAdmin):
    pass


@admin.register(ServicePart)
class ServicePartAdmin(ModelAdmin):
    pass


@admin.register(ServiceActivity)
class ServiceActivityAdmin(ModelAdmin):
    pass


@admin.register(EmailSent)
class EmailSentAdmin(ModelAdmin):
    pass
