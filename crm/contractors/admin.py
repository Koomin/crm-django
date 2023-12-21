from django.contrib import admin
from django.contrib.admin import ModelAdmin

from crm.contractors.models import Contractor


@admin.register(Contractor)
class ContractorAdmin(ModelAdmin):
    pass
