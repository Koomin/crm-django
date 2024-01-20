from django.contrib import admin
from django.contrib.admin import ModelAdmin

from crm.service.models import Category, Device, DeviceType, Note, OrderType, ServiceOrder, Stage


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    pass


@admin.register(Stage)
class StageAdmin(ModelAdmin):
    pass


@admin.register(DeviceType)
class DeviceTypeAdmin(ModelAdmin):
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
