from django.contrib.admin.models import LogEntry
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

from crm.core.api.views import BaseViewSet
from crm.crm_config.api.serializers import (
    CountrySerializer,
    EmailTemplateSerializer,
    GeneralSettingsSerializer,
    LogEntrySerializer,
    LogSerializer,
    ServiceAddressSerializer,
    StateSerializer,
    TaxPercentageSerializer,
)
from crm.crm_config.models import Country, EmailTemplate, GeneralSettings, Log, ServiceAddress, State, TaxPercentage


class CountryViewSet(ListModelMixin, BaseViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAuthenticated | HasAPIKey]


class StateViewSet(ListModelMixin, BaseViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = [IsAuthenticated | HasAPIKey]


class EmailTemplateViewSet(ListModelMixin, CreateModelMixin, UpdateModelMixin, BaseViewSet):
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class GeneralSettingsViewSet(ListModelMixin, UpdateModelMixin, BaseViewSet):
    queryset = GeneralSettings.objects.all()
    serializer_class = GeneralSettingsSerializer

    def list(self, request, *args, **kwargs):
        queryset = GeneralSettings.objects.all().first()
        serializer = GeneralSettingsSerializer(queryset)
        return Response(serializer.data)


class LogViewSet(ListModelMixin, BaseViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer


class LogEntryViewSet(ListModelMixin, viewsets.GenericViewSet):
    queryset = LogEntry.objects.all()
    serializer_class = LogEntrySerializer


class TaxPercentageViewSet(ListModelMixin, BaseViewSet):
    queryset = TaxPercentage.objects.all()
    serializer_class = TaxPercentageSerializer


class ServiceAddressViewSet(ListModelMixin, BaseViewSet):
    queryset = ServiceAddress.objects.all()
    serializer_class = ServiceAddressSerializer
    permission_classes = [IsAuthenticated | HasAPIKey]
