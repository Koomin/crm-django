from django.contrib import admin

from crm.service.models import Attribute, AttributeDefinition


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
