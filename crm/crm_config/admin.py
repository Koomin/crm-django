from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.admin.models import LogEntry

from crm.crm_config.models import (
    Country,
    EmailTemplate,
    GeneralSettings,
    Import,
    Log,
    ServiceAddress,
    State,
    TaxPercentage,
)


@admin.register(State)
class StateAdmin(ModelAdmin):
    pass


@admin.register(Country)
class CountryAdmin(ModelAdmin):
    pass


@admin.register(EmailTemplate)
class EmailTemplateAdmin(ModelAdmin):
    pass


@admin.register(GeneralSettings)
class GeneralSettingsAdmin(ModelAdmin):
    pass


@admin.register(Log)
class LogAdmin(ModelAdmin):
    pass


@admin.register(LogEntry)
class LogEntryAdmin(ModelAdmin):
    pass


@admin.register(TaxPercentage)
class TaxPercentageAdmin(ModelAdmin):
    pass


@admin.register(ServiceAddress)
class ServiceAddressAdmin(ModelAdmin):
    pass


@admin.register(Import)
class ImportAdmin(ModelAdmin):
    pass
