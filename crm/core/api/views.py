import django_filters
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class BasePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 1000


class BaseViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "uuid"
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ["uuid"]
    pagination_class = BasePagination

    @action(detail=False, methods=["get"])
    def all(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data)

    def get_queryset(self):
        return super().get_queryset().order_by("-created")
