import io

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

from crm.contractors.models import Contractor
from crm.core.api.mixins import OptimaUpdateModelMixin
from crm.core.api.views import BaseViewSet
from crm.crm_config.models import Country, Log
from crm.service.api.serializers import (
    AttributeDefinitionItemSerializer,
    AttributeDefinitionSerializer,
    AttributeSerializer,
    CategorySerializer,
    DeviceCatalogSerializer,
    DeviceSerializer,
    DeviceTypeSerializer,
    EmailSentSerializer,
    NewServiceOrderSerializer,
    NoteSerializer,
    OrderTypeSerializer,
    PurchaseDocumentSerializer,
    ServiceActivityReadSerializer,
    ServiceActivitySerializer,
    ServiceOrderSerializer,
    StageDurationSerializer,
    StageSerializer,
    StageUpdateSerializer,
)
from crm.service.models import (
    Attribute,
    AttributeDefinition,
    AttributeDefinitionItem,
    Category,
    Device,
    DeviceCatalog,
    DeviceType,
    EmailSent,
    Note,
    OrderType,
    ServiceActivity,
    ServiceOrder,
    Stage,
    StageDuration,
)
from crm.shipping.models import Shipping, ShippingAddress, ShippingMethod


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


class DeviceCatalogViewSet(ListModelMixin, RetrieveModelMixin, BaseViewSet):
    queryset = DeviceCatalog.objects.all()
    permission_classes = [IsAuthenticated | HasAPIKey]
    serializer_class = DeviceCatalogSerializer


class DeviceTypeViewSet(ListModelMixin, RetrieveModelMixin, BaseViewSet):
    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer


class DeviceViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, BaseViewSet):
    queryset = Device.objects.all()
    permission_classes = [IsAuthenticated | HasAPIKey]
    serializer_class = DeviceSerializer
    filterset_fields = ["uuid", "device_catalog__uuid"]


class NoteViewSet(ListModelMixin, RetrieveModelMixin, OptimaUpdateModelMixin, CreateModelMixin, BaseViewSet):
    queryset = Note.objects.all().order_by("-date")
    serializer_class = NoteSerializer
    filterset_fields = ["uuid", "service_order__uuid"]

    def create(self, request, *args, **kwargs):
        request.data["user"] = self.request.user.pk
        return super().create(request, *args, **kwargs)


class OrderTypeViewSet(ListModelMixin, UpdateModelMixin, RetrieveModelMixin, BaseViewSet):
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
            else:
                exported = order.export()
                if exported:
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
            # Moved to new service order creation
            # request.data["acceptance_date"] = timezone.now()
            request.data["user"] = request.user.uuid
            try:
                default_stage = Stage.objects.get(is_default=True)
            except (Stage.DoesNotExist, MultipleObjectsReturned) as e:
                Log.objects.create(
                    exception_traceback=e,
                    method_name="partial_update",
                    model_name=self.__class__.__name__,
                )
            else:
                request.data["stage"] = default_stage.uuid
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
                current_stage_duration.end = timezone.now()
                current_stage_duration.save()
            new_stage = Stage.objects.get(uuid=request.data.get("stage"))
            StageDuration.objects.get_or_create(stage=new_stage, service_order=service_order)
            for attr in new_stage.attributes.all():
                try:
                    attribute = Attribute.objects.get(service_order=service_order, attribute_definition=attr)
                except Attribute.DoesNotExist:
                    pass
                else:
                    if attribute.value:
                        pass
                    else:
                        attribute.value = timezone.now().date().strftime("%Y-%m-%d")
                        attribute.save()
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

    @permission_classes(
        [
            AllowAny,
        ]
    )
    @action(detail=True, methods=["get"])
    def images(self, request, uuid):
        obj = get_object_or_404(ServiceOrder, uuid=uuid)
        form_files = obj.form_files.all()
        mem_zip = io.BytesIO()
        import zipfile

        with zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            for f in form_files:
                file_to_zip = open(f.file.path, "rb")
                try:
                    zf.writestr(f.file.name.split("/")[-1], file_to_zip.getvalue())
                except AttributeError:
                    zf.writestr(f.file.name.split("/")[-1], file_to_zip.read())
        mem_zip = mem_zip.getvalue()
        response = HttpResponse(mem_zip, content_type="application/zip")
        return response


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
        data["acceptance_date"] = timezone.now()
        try:
            contractor_country = Country.objects.get(uuid=data.get("contractor_country"))
        except Country.DoesNotExist:
            contractor_country = None
            data["contractor_country"] = ""
        else:
            data["contractor_country"] = contractor_country.name
        if data.get("tax_number", None) and data.get("tax_number") != "":
            customer_dict = {}
            for k, v in data.items():
                if "contractor_" in k:
                    if k not in ["contractor_type", "contractor_country_name"]:
                        customer_dict[k.replace("contractor_", "")] = v
            try:
                contractor = Contractor.objects.get(tax_number=data["tax_number"])
            except Contractor.DoesNotExist:
                contractor = Contractor(tax_number=data["tax_number"], **customer_dict)
                contractor.save_without_optima_export()
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
        try:
            device = Device.objects.get(uuid=data.get("device"))
        except Device.DoesNotExist:
            device = None
        description = ""
        model_contractor = f'{device.name}; {data.get("contractor_name")}\n'
        description += model_contractor
        if data.get("purchase_document_number"):
            description += f'\nDowód zakupu: {data.get("purchase_document_number")} '
        if data.get("purchase_date"):
            description += f'{data.get("purchase_date")}\n'
        shipping = Shipping()
        shipping_address = ShippingAddress()
        if data.get("shipping") == "delivery_company":
            shipping.default_send = True
        if data.get("shipping_country"):
            try:
                shipping_address.country = Country.objects.get(uuid=data.get("shipping_country"))
            except Country.DoesNotExist:
                shipping_address.country = None
            shipping_address.city = data.get("shipping_city")
            shipping_address.home_number = (
                data.get("shipping_home_number") if data.get("shipping_home_number") else None
            )
            shipping_address.postal_code = data.get("shipping_postal_code")
            shipping_address.street = data.get("shipping_street")
            shipping_address.street_number = data.get("shipping_street_number")
            shipping_address.name = data.get("contractor_name")
        else:
            shipping_address.city = data.get("contractor_city")
            shipping_address.country = contractor_country
            shipping_address.home_number = (
                data.get("contractor_home_number") if data.get("contractor_home_number") else None
            )
            shipping_address.postal_code = data.get("contractor_postal_code")
            shipping_address.street = data.get("contractor_street")
            shipping_address.street_number = data.get("contractor_street_number")
            shipping_address.name = data.get("contractor_name")
        if data.get("shipping_method"):
            shipping.shipping_method = ShippingMethod.objects.get(uuid=data.get("shipping_method"))
            shipping.shipping_company = shipping.shipping_method.company
        shipping_address.save()
        shipping.address = shipping_address
        address = (
            f"Adres do obioru/wysyłki urządzenia:\n{shipping_address.street} {shipping_address.street_number}"
            f"{'/' + shipping_address.home_number if shipping_address.home_number else ''}\n"
            f"{shipping_address.postal_code} {shipping_address.city}\n"
        )
        description += address
        description += f'Opis usterki:\n{data.get("description")}'
        data["description"] = description
        data["document_date"] = timezone.now()
        try:
            OrderType.objects.get(uuid=data["order_type"])
        except ObjectDoesNotExist:
            return Response("Nie znaleziono typu zgłoszenia.", status=status.HTTP_404_NOT_FOUND)
        try:
            data["category"] = Category.objects.get(code="200").pk
        except Category.DoesNotExist:
            pass

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        from crm.service.tasks import email_order_created

        email_order_created.apply_async()
        shipping.service_order = instance
        shipping.save()
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


class AttributeDefinitionViewSet(ListModelMixin, BaseViewSet):
    queryset = AttributeDefinition.objects.all()
    serializer_class = AttributeDefinitionSerializer

    @action(detail=False, methods=["get"])
    def active(self, request):
        queryset = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data)


class StageDurationViewSet(ListModelMixin, BaseViewSet):
    queryset = StageDuration.objects.all()
    serializer_class = StageDurationSerializer
    filterset_fields = ["uuid", "service_order__uuid"]


class ServiceActivityViewSet(ListModelMixin, CreateModelMixin, OptimaUpdateModelMixin, BaseViewSet):
    queryset = ServiceActivity.objects.all()
    serializer_class = ServiceActivitySerializer
    list_serializer_class = ServiceActivityReadSerializer
    filterset_fields = ["uuid", "service_order__uuid"]

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        try:
            service_order = ServiceOrder.objects.get(uuid=request.data["service_order"])
        except ServiceOrder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        all_activities_numbers = service_order.service_activities.filter(number__isnull=False).values_list(
            "number", flat=True
        )
        last_number = max(all_activities_numbers) if all_activities_numbers else 0
        request.data["number"] = last_number + 1
        request.data["user"] = request.user.optima_user.uuid
        return super().create(request, *args, **kwargs)


class EmailSentViewSet(ListModelMixin, BaseViewSet):
    queryset = EmailSent.objects.all()
    serializer_class = EmailSentSerializer
    filterset_fields = ["uuid", "service_order__uuid"]
