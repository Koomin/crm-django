import django_filters
from rest_framework import permissions, viewsets


class BaseViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "uuid"
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ["uuid"]
