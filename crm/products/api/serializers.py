from rest_framework import serializers

from crm.products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["uuid", "code", "name", "unit", "type"]
