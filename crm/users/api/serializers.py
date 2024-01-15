import json

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

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
                ],
                "actions": {},
            }
        )
        return data


class UserSerializer(
    serializers.ModelSerializer[UserType],
):
    class Meta:
        model = User
        fields = ["uuid", "username", "first_name", "last_name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "uuid"},
        }
