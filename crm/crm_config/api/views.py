from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from crm.core.api.views import BaseViewSet
from crm.crm_config.api.serializers import (
    CountrySerializer,
    EmailTemplateSerializer,
    GeneralSettingsSerializer,
    StateSerializer,
)
from crm.crm_config.models import Country, EmailTemplate, GeneralSettings, State


class CountryViewSet(ListModelMixin, BaseViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class StateViewSet(ListModelMixin, BaseViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class EmailTemplateViewSet(ListModelMixin, CreateModelMixin, UpdateModelMixin, BaseViewSet):
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class GeneralSettingsViewSet(ListModelMixin, UpdateModelMixin, BaseViewSet):
    queryset = GeneralSettings.objects.all()
    serializer_class = GeneralSettingsSerializer
    permission_classes = [IsAuthenticated]
