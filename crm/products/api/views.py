from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response

from crm.core.api.views import BaseViewSet
from crm.products.api.serializers import ProductSerializer
from crm.products.models import Product


class ProductViewSet(ListModelMixin, BaseViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = [
        "uuid",
    ]

    @action(detail=False)
    def services(self, request):
        qs = self.get_queryset().filter(type=Product.ProductType.SERVICE)
        serializer = self.get_serializer(qs, many=True)
        return Response(data=serializer.data)

    @action(detail=False)
    def products(self, request):
        qs = self.get_queryset().filter(type=Product.ProductType.PRODUCT)
        serializer = self.get_serializer(qs, many=True)
        return Response(data=serializer.data)
