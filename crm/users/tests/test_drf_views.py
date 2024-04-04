import pytest
from rest_framework.test import APIRequestFactory

from crm.users.api.serializers import OptimaUserSerializer
from crm.users.api.views import OptimaUserViewSet, UserViewSet
from crm.users.models import OptimaUser, User


class TestUserViewSet:
    @pytest.fixture
    def api_rf(self) -> APIRequestFactory:
        return APIRequestFactory()

    def test_get_queryset(self, user: User, api_rf: APIRequestFactory):
        view = UserViewSet()
        request = api_rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert user in view.get_queryset()

    def test_me(self, user: User, api_rf: APIRequestFactory):
        view = UserViewSet()
        request = api_rf.get("/fake-url/")
        request.user = user

        view.request = request

        response = view.me(request)  # type: ignore
        assert response.data == {
            "uuid": user.uuid,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "url": f"http://testserver/api/v1/users/{user.uuid}/",
            "optima_user": user.optima_user.uuid,
            "optima_user_code": user.optima_user.code,
            "optima_user_name": user.optima_user.name,
            "optima_user_full": OptimaUserSerializer(user.optima_user).data,
        }


class TestOptimaUserViewSet:
    @pytest.fixture
    def api_rf(self) -> APIRequestFactory:
        return APIRequestFactory()

    def test_get_queryset(self, user: User, optima_user: OptimaUser, api_rf: APIRequestFactory):
        view = OptimaUserViewSet()
        request = api_rf.get("/fake-url/")
        request.user = user
        view.request = request

        assert optima_user in view.get_queryset()
