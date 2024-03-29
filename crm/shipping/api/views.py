from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import ListModelMixin, UpdateModelMixin
from rest_framework.response import Response

from crm.core.api.views import BaseViewSet
from crm.shipping.api.serializers import ShippingAddressUpdateSerializer, ShippingSerializer
from crm.shipping.models import Shipping, ShippingAddress


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
        qs = self.queryset.filter(is_sent=False, service_order__full_number__isnull=False)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(data=serializer.data)

    @action(detail=True, methods=["post"])
    def send(self, request, uuid):
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

    @action(detail=True, methods=["get"])
    def label(self, request, uuid):
        obj = get_object_or_404(Shipping, uuid=uuid)
        with open(obj.label.path, "rb") as pdf_file:
            response = HttpResponse(pdf_file.read(), headers={"Content-Type": "application/pdf"})
        return response


class ShippingAddressViewSet(UpdateModelMixin, BaseViewSet):
    queryset = ShippingAddress.objects.all()
    serializer_class = ShippingAddressUpdateSerializer
