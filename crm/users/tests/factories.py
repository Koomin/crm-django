from collections.abc import Sequence
from typing import Any

from django.contrib.auth import get_user_model
from factory import Faker, SubFactory, post_generation
from factory.django import DjangoModelFactory

from crm.users.models import OptimaUser


class OptimaUserFactory(DjangoModelFactory):
    uuid = Faker("uuid4")
    optima_id = Faker("random_number")
    name = Faker("name")
    code = Faker("pystr", max_chars=50)
    exported = Faker("pybool")
    created = Faker("date_time_this_year")
    modified = Faker("date_time_this_year")

    class Meta:
        model = OptimaUser


class UserFactory(DjangoModelFactory):
    uuid = Faker("uuid4")
    username = Faker("user_name")
    email = Faker("email")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    optima_user = SubFactory(OptimaUserFactory)
    created = Faker("date_time_this_year")

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).evaluate(None, None, extra={"locale": None})
        )
        self.set_password(password)

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        """Save again the instance if creating and at least one hook ran."""
        if create and results and not cls._meta.skip_postgeneration_save:
            # Some post-generation hooks ran, and may have modified us.
            instance.save()

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]
