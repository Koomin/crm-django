import datetime

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

from crm.contractors.models import Contractor
from crm.core.api.mixins import OptimaUpdateModelMixin
from crm.core.api.views import BaseViewSet
from crm.service.api.serializers import (
    AttributeDefinitionItemSerializer,
    AttributeSerializer,
    CategorySerializer,
    DeviceSerializer,
    DeviceTypeSerializer,
    EmailSentSerializer,
    NewServiceOrderSerializer,
    NoteSerializer,
    OrderTypeSerializer,
    PurchaseDocumentSerializer,
    ServiceActivitySerializer,
    ServiceOrderSerializer,
    StageDurationSerializer,
    StageSerializer,
    StageUpdateSerializer,
)
from crm.service.models import (
    Attribute,
    AttributeDefinitionItem,
    Category,
    Device,
    DeviceType,
    EmailSent,
    Note,
    OrderType,
    ServiceActivity,
    ServiceOrder,
    Stage,
    StageDuration,
)


class CategoryViewSet(ListModelMixin, RetrieveModelMixin, BaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class StageViewSet(ListModelMixin, UpdateModelMixin, RetrieveModelMixin, BaseViewSet):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer
    update_serializer_class = StageUpdateSerializer

    def get_serializer_class(self):
        if self.action == "partial_update":
            return self.update_serializer_class
        return self.serializer_class


class DeviceTypeViewSet(ListModelMixin, RetrieveModelMixin, BaseViewSet):
    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer


class DeviceViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, BaseViewSet):
    queryset = Device.objects.all()
    permission_classes = [IsAuthenticated | HasAPIKey]
    serializer_class = DeviceSerializer


class NoteViewSet(ListModelMixin, RetrieveModelMixin, OptimaUpdateModelMixin, CreateModelMixin, BaseViewSet):
    queryset = Note.objects.all().order_by("-date")
    serializer_class = NoteSerializer
    filterset_fields = ["uuid", "service_order__uuid"]

    def create(self, request, *args, **kwargs):
        request.data["user"] = self.request.user.pk
        return super().create(request, *args, **kwargs)


class OrderTypeViewSet(ListModelMixin, RetrieveModelMixin, BaseViewSet):
    permission_classes = [IsAuthenticated | HasAPIKey]
    queryset = OrderType.objects.all()
    serializer_class = OrderTypeSerializer


class ServiceOrderViewSet(ListModelMixin, RetrieveModelMixin, OptimaUpdateModelMixin, BaseViewSet):
    queryset = ServiceOrder.objects.all().order_by("-document_date")
    serializer_class = ServiceOrderSerializer
    filterset_fields = ["uuid", "state"]

    @action(detail=True, methods=["post"])
    def synchronize(self, request, uuid):
        try:
            order = self.queryset.get(uuid=uuid)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            from crm.service.tasks import synchronize_order

            if order.optima_id:
                synchronize_order.apply_async(args=[order.optima_id])
                return Response(status=status.HTTP_200_OK)
            return Response(data="Zlecenie nie wyeksportowane do Optima", status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=["post"])
    def export(self, uuid):
        try:
            order = self.queryset.filter(uuid=uuid)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        created = order.export()
        if created:
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, *args, **kwargs):
        if request.data.get("state") == 0:
            request.data["acceptance_date"] = datetime.datetime.now()
        if request.data.get("stage"):
            try:
                service_order = ServiceOrder.objects.get(uuid=kwargs.get("uuid"))
            except ServiceOrder.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            current_stage = service_order.stage
            try:
                current_stage_duration = StageDuration.objects.get(stage=current_stage, service_order=service_order)
            except StageDuration.DoesNotExist:
                pass
            else:
                current_stage_duration.end = datetime.datetime.now()
                current_stage_duration.save()
            new_stage = Stage.objects.get(uuid=request.data.get("stage"))
            StageDuration.objects.get_or_create(stage=new_stage, service_order=service_order)
        # Moved to ServiceOrder save method.
        # if request.data.get("document_type"):
        #     try:
        #         document_type = DocumentType.objects.get(uuid=request.data.get("document_type"))
        #     except Exception:
        #         return Response(status=status.HTTP_404_NOT_FOUND)
        #     number_scheme = document_type.format_numbering_scheme()
        #     request.data["number_scheme"] = number_scheme
        return super().partial_update(request, *args, **kwargs)

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
        qs = self.queryset.filter(state=3)
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
    queryset = ServiceOrder.objects.filter(state=99)
    serializer_class = NewServiceOrderSerializer
    permission_classes = [IsAuthenticated | HasAPIKey]

    def create(self, request, *args, **kwargs):
        # TODO ADD STAGE WHILE CREATING NEW ORDER
        data = request.data.copy()
        if data.get("tax_number", None) and data.get("tax_number") != "":
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
        if data.get("contractor_name"):
            if len(data.get("contractor_name")) > 50:
                data["contractor_name1"] = data.get("contractor_name")[:50]
                if len(data.get("contractor_name")) > 100:
                    data["contractor_name2"] = data.get("contractor_name")[51:100]
                    data["contractor_name3"] = data.get("contractor_name")[100:]
                else:
                    data["contractor_name2"] = data.get("contractor_name")[51:]
            else:
                data["contractor_name1"] = data.get("contractor_name")
        description = data.get("description")
        if not description:
            description = ""
        description += "\nDane z formularza:\n"
        purchase_data = (
            f'\nNumer dokumentu sprzedaży: {data.get("purchase_document_number")}, '
            f'data sprzedaży: {data.get("purchase_date")}\n'
        )
        description += purchase_data
        address = (
            f'Adres do wysyłki: ul.{data.get("contractor_street")} {data.get("contractor_home_number")}\n'
            f'{data.get("contractor_postal_code")} {data.get("contractor_city")}\n'
            f'{data.get("contractor_country")}\n'
        )
        description += address
        data["description"] = description
        data["document_date"] = datetime.datetime.now()
        try:
            OrderType.objects.get(uuid=data["order_type"])
        except ObjectDoesNotExist:
            return Response("Nie znaleziono typu zgłoszenia.", status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AttributeViewSet(ListModelMixin, OptimaUpdateModelMixin, BaseViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    filterset_fields = ["uuid", "service_order__uuid"]


class AttributeDefinitionItemViewSet(ListModelMixin, BaseViewSet):
    queryset = AttributeDefinitionItem.objects.all()
    serializer_class = AttributeDefinitionItemSerializer
    filterset_fields = ["uuid", "attribute_definition__uuid"]


class StageDurationViewSet(ListModelMixin, BaseViewSet):
    queryset = StageDuration.objects.all()
    serializer_class = StageDurationSerializer
    filterset_fields = ["uuid", "stage_duration__uuid", "service_order__uuid"]


class ServiceActivityViewSet(ListModelMixin, CreateModelMixin, OptimaUpdateModelMixin, BaseViewSet):
    queryset = ServiceActivity.objects.all()
    serializer_class = ServiceActivitySerializer
    filterset_fields = ["uuid", "service_order__uuid"]

    def create(self, request, *args, **kwargs):
        try:
            service_order = ServiceOrder.objects.get(uuid=request.data["service_order"])
        except ServiceOrder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        last_number = max(
            service_order.service_activities.filter(number__isnull=False).values_list("number", flat=True)
        )
        request.data["number"] = last_number + 1
        return super().create(request, *args, **kwargs)


class EmailSentViewSet(ListModelMixin, BaseViewSet):
    queryset = EmailSent.objects.all()
    serializer_class = EmailSentSerializer
    filterset_fields = ["uuid", "service_order__uuid"]
