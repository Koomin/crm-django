from rest_framework import permissions, viewsets


class BaseViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "uuid"
