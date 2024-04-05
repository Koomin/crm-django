from django.test import TestCase

from crm.users.models import User
from crm.users.tests.factories import OptimaUserFactory


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/users/{user.username}/"


class OptimaUserTest(TestCase):
    def create_user(self):
        return OptimaUserFactory()

    def test_optima_user_str(self):
        user = self.create_user()
        self.assertEqual(str(user), user.__str__())
        self.assertEqual(f"{user.name} ({user.code})", user.__str__())
