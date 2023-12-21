from django.db import models

from crm.core.models import OptimaModel


class Warehouse(OptimaModel):
    class Types(models.IntegerChoices):
        LOCAL = 1, "Local"
        DISTANT = 2, "Distant"
        SERVICE = 3, "Service"
        MOBILE = 4, "Mobile"

    type = models.IntegerField(choices=Types.choices, default=Types.LOCAL)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)
    symbol = models.CharField(max_length=55)
    register = models.CharField(max_length=20)
    active = models.BooleanField(default=True)
