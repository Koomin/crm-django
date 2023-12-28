from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from crm.contractors.api.serializers import ContractorSerializer
from crm.contractors.models import Contractor
from crm.core.api.views import BaseViewSet


class ContractorViewSet(ListModelMixin, RetrieveModelMixin, BaseViewSet):
    queryset = Contractor.objects.all()
    serializer_class = ContractorSerializer
