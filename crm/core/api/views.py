import django_filters
from rest_framework import permissions, viewsets
from rest_framework.pagination import PageNumberPagination


class BasePagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000


class BaseViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "uuid"
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ["uuid"]
    pagination_class = BasePagination
