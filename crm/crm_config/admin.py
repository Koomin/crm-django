from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.admin.models import LogEntry

from crm.crm_config.models import Country, EmailTemplate, GeneralSettings, Log, State


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
