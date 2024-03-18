import uuid as uuid_lib

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField, OneToOneField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from crm.core.models import OptimaModel
from crm.permissions.models import GroupPermission, ViewPermission


class OptimaUser(OptimaModel):
    name = models.CharField(_("Name"), max_length=1024)
    code = models.CharField(_("Code"), max_length=50)

    def __str__(self):
        return f"{self.name} ({self.code})"


class User(AbstractUser):
    """
    Default custom user model for CRM.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    first_name = CharField(_("Name of User"), blank=True, max_length=255)
    last_name = CharField(_("Last Name of User"), blank=True, max_length=255)
    optima_user = OneToOneField(OptimaUser, on_delete=models.CASCADE, null=True, related_name="user")
    created = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(GroupPermission, on_delete=models.CASCADE, null=True, related_name="users", blank=True)
    view_permissions = models.ManyToManyField(ViewPermission)

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    def get_permission(self) -> dict:
        if self.group:
            perm_list = [perm.view for perm in self.group.view_permissions.all()]
        else:
            perm_list = []
        if self.view_permissions.exists():
            perm_list.extend([perm.view for perm in self.view_permissions.all()])
        perm_list = list(set(perm_list))
        return {
            "models": perm_list,
            "actions": {},
            "is_superuser": self.is_superuser,
        }
