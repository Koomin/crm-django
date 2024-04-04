from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response

from crm.contractors.api.serializers import ContractorSerializer
from crm.contractors.models import Contractor
from crm.core.api.views import BaseViewSet


class ContractorViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, BaseViewSet):
    queryset = Contractor.objects.all()
    serializer_class = ContractorSerializer

    @action(detail=False)
    def confirmed(self, request):
        qs = self.get_queryset().filter(confirmed=True)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(data=serializer.data)

    @action(detail=False)
    def unconfirmed(self, request):
        qs = self.get_queryset().filter(confirmed=False)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(data=serializer.data)
