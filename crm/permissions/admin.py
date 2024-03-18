from django.contrib import admin

from crm.permissions.models import GroupPermission, ViewPermission


@admin.register(GroupPermission)
class GroupPermissionAdmin(admin.ModelAdmin):
    pass


@admin.register(ViewPermission)
class ViewPermissionAdmin(admin.ModelAdmin):
    pass
