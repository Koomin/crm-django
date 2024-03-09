import json

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from crm.users.models import OptimaUser
from crm.users.models import User as UserType

User = get_user_model()


class TokenWithUserObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = {"first_name": self.user.first_name, "last_name": self.user.last_name}
        # data['permissions'] = self.user.get_permission_table()
        data["permissions"] = json.dumps(
            {
                "models": [
                    "Dashboard",
                    "NewCustomers",
                    "Customers",
                    "ServiceOrders",
                    "AcceptedServiceOrders",
                    "OngoingServiceOrders",
                    "RejectedServiceOrders",
                    "ClosedServiceOrders",
                    "Users",
                    "Settings",
                    "Connections",
                    "Mailing",
                    "GeneralSettings",
                ],
                "actions": {},
            }
        )
        return data


class TokenWithUserRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # data['user'] = {'first_name': self.user.first_name, 'last_name': self.user.last_name}
        # data['permissions'] = self.user.get_permission_table()
        data["permissions"] = json.dumps(
            {
                "models": [
                    "Dashboard",
                    "Customers",
                    "ServiceOrders",
                    "NewServiceOrders",
                    "OngoingServiceOrders",
                    "RejectedServiceOrders",
                    "ClosedServiceOrders",
                    "Users",
                    "Settings",
                ],
                "actions": {},
            }
        )
        return data


class OptimaUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptimaUser
        fields = ["uuid", "name", "code"]


class UserSerializer(serializers.ModelSerializer[UserType]):
    optima_user = serializers.SlugRelatedField(slug_field="uuid", queryset=OptimaUser.objects.all(), read_only=False)
    optima_user_name = serializers.CharField(source="optima_user.name", read_only=True)
    optima_user_code = serializers.CharField(source="optima_user.code", read_only=True)
    optima_user_full = OptimaUserSerializer(source="optima_user", read_only=True)

    class Meta:
        model = User
        fields = [
            "uuid",
            "username",
            "first_name",
            "last_name",
            "url",
            "optima_user",
            "optima_user_code",
            "optima_user_name",
            "optima_user_full",
        ]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "uuid"},
        }
