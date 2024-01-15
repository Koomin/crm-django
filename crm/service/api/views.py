from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response

from crm.core.api.views import BaseViewSet
from crm.service.api.serializers import (
    CategorySerializer,
    DeviceSerializer,
    DeviceTypeSerializer,
    ServiceOrderSerializer,
    StageSerializer,
)
from crm.service.models import Category, Device, DeviceType, ServiceOrder, Stage


class CategoryViewSet(ListModelMixin, RetrieveModelMixin, BaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class StageViewSet(ListModelMixin, RetrieveModelMixin, BaseViewSet):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer


class DeviceTypeViewSet(ListModelMixin, RetrieveModelMixin, BaseViewSet):
    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer


class DeviceViewSet(ListModelMixin, RetrieveModelMixin, BaseViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class ServiceOrderViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, BaseViewSet):
    queryset = ServiceOrder.objects.all().order_by("-document_date")
    serializer_class = ServiceOrderSerializer
    filterset_fields = ["uuid", "state"]

    @action(detail=False)
    def ongoing(self, request):
        qs = self.queryset.filter(state=1)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(data=serializer.data)

    @action(detail=False)
    def accepted(self, request):
        qs = self.queryset.filter(state=0)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(data=serializer.data)

    @action(detail=False)
    def realized(self, request):
        qs = self.queryset.filter(state=2)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(data=serializer.data)

    @action(detail=False)
    def rejected(self, request):
        qs = self.queryset.filter(state=2)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(data=serializer.data)

    @action(detail=False)
    def new(self, request):
        qs = self.queryset.filter(optima_id__isnull=True)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(data=serializer.data)
