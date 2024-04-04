from django.contrib import admin
from django.contrib.admin import ModelAdmin

from crm.products.models import Product


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    pass
