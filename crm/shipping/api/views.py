from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response

from crm.core.api.views import BaseViewSet
from crm.shipping.api.serializers import ShippingSerializer
from crm.shipping.models import Shipping


class ShippingViewSet(ListModelMixin, BaseViewSet):
    queryset = Shipping.objects.all()
    serializer_class = ShippingSerializer

    @action(detail=False)
    def completed(self, request):
        qs = self.queryset.filter(is_sent=True)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(data=serializer.data)

    @action(detail=False)
    def awaiting(self, request):
        qs = self.queryset.filter(is_sent=False)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(data=serializer.data)

    @action(detail=False, methods=["post"])
    def send(self, uuid):
        try:
            obj = Shipping.objects.get(uuid=uuid)
        except Shipping.DoesNotExist:
            pass
        else:
            if obj.is_sent:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            sent = obj.send()
            if sent:
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
