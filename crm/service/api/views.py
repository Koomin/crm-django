from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

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


class ServiceOrderViewSet(ListModelMixin, RetrieveModelMixin, BaseViewSet):
    queryset = ServiceOrder.objects.all()
    serializer_class = ServiceOrderSerializer
