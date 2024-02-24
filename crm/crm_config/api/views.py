from rest_framework.mixins import ListModelMixin

from crm.core.api.views import BaseViewSet
from crm.crm_config.api.serializers import CountrySerializer, StateSerializer
from crm.crm_config.models import Country, State


class CountryViewSet(ListModelMixin, BaseViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class StateViewSet(ListModelMixin, BaseViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer
