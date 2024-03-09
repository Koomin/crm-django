from django.contrib import admin
from django.contrib.admin import ModelAdmin

from crm.crm_config.models import Country, EmailTemplate, GeneralSettings, State


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
