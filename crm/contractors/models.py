from django.db import models

from crm.core.models import OptimaModel


class Contractor(OptimaModel):
    code = models.CharField(max_length=120, null=False)
    postal_code = models.CharField(max_length=20)
    tax_number = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=120)
    street = models.CharField(max_length=200)
    street_number = models.CharField(max_length=12)
    home_number = models.IntegerField(null=True)
    post = models.CharField(max_length=120)
    state = models.CharField(max_length=40)
    name = models.CharField(max_length=1024)
