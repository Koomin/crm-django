from django.contrib import admin
from django.contrib.admin import ModelAdmin

from crm.documents.models import DocumentType


@admin.register(DocumentType)
class DocumentTypeAdmin(ModelAdmin):
    pass
