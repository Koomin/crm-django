from rest_framework.mixins import ListModelMixin

from crm.core.api.views import BaseViewSet
from crm.products.api.serializers import ProductSerializer
from crm.products.models import Product


class ProductViewSet(ListModelMixin, BaseViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = [
        "uuid",
    ]
