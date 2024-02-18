from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from crm.core.api.views import BaseViewSet

from ..models import OptimaUser
from .serializers import (
    OptimaUserSerializer,
    TokenWithUserObtainPairSerializer,
    TokenWithUserRefreshSerializer,
    UserSerializer,
)

User = get_user_model()


class UserViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, UpdateModelMixin, BaseViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    # def get_queryset(self, *args, **kwargs):
    #     assert isinstance(self.request.user.id, int)
    #     return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class OptimaUserViewSet(ListModelMixin, BaseViewSet):
    serializer_class = OptimaUserSerializer
    queryset = OptimaUser.objects.all()


class TokenWithUserObtainPairView(TokenObtainPairView):
    serializer_class = TokenWithUserObtainPairSerializer


class TokenWithUserRefreshView(TokenRefreshView):
    serializer_class = TokenWithUserRefreshSerializer
