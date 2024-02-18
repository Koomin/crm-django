from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from crm.contractors.models import Contractor
from crm.core.api.views import BaseViewSet
from crm.service.api.serializers import (
    CategorySerializer,
    DeviceSerializer,
    DeviceTypeSerializer,
    NewServiceOrderSerializer,
    NoteSerializer,
    OrderTypeSerializer,
    PurchaseDocumentSerializer,
    ServiceOrderSerializer,
    StageSerializer,
)
from crm.service.models import Category, Device, DeviceType, Note, OrderType, ServiceOrder, Stage


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


class NoteViewSet(ListModelMixin, RetrieveModelMixin, BaseViewSet):
    queryset = Note.objects.all().order_by("-date")
    serializer_class = NoteSerializer
    filterset_fields = ["uuid", "service_order__uuid"]


class OrderTypeViewSet(ListModelMixin, RetrieveModelMixin, BaseViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = OrderType.objects.all()
    serializer_class = OrderTypeSerializer


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
        qs = self.queryset.filter(state=99)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(data=serializer.data)


class PurchaseDocumentViewSet(ListModelMixin, BaseViewSet):
    queryset = ServiceOrder.objects.filter(purchase_document__isnull=False)
    serializer_class = PurchaseDocumentSerializer
    filterset_fields = ["uuid"]


class NewServiceOrderViewSet(UpdateModelMixin, CreateModelMixin, BaseViewSet):
    queryset = ServiceOrder.objects.filter(state=99).order_by("-document_date")
    serializer_class = NewServiceOrderSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        data = request.data
        if data.get("tax_number", None):
            customer_dict = {}
            for k, v in data.items():
                if "contractor_" in k:
                    customer_dict[k.replace("contractor_", "")] = v
            contractor, created = Contractor.objects.get_or_create(
                tax_number=data["tax_number"], defaults=customer_dict
            )
            data["contractor"] = contractor.uuid
        else:
            try:
                contractor = Contractor.objects.get(code="FIZYCZNA")
            except ObjectDoesNotExist:
                return Response("Nie znaleziono kontrahenta.", status=status.HTTP_404_NOT_FOUND)
            else:
                data["contractor"] = contractor.uuid
                data["contractor_name"] = f'{data.pop("first_name")[0]} {data.pop("last_name")[0]}'
        try:
            OrderType.objects.get(uuid=data["order_type"])
        except ObjectDoesNotExist:
            return Response("Nie znaleziono typu zgłoszenia.", status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
