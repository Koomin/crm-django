from django.db import models

from crm.core.models import OptimaModel


class Contractor(OptimaModel):
    code = models.CharField(max_length=120, null=True, blank=True)
    postal_code = models.CharField(max_length=20)
    tax_number = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=120)
    street = models.CharField(max_length=200)
    street_number = models.CharField(max_length=12)
    home_number = models.IntegerField(null=True, blank=True)
    post = models.CharField(max_length=120)
    state = models.CharField(max_length=40)
    name = models.CharField(max_length=1024)
    name1 = models.CharField(max_length=1024)
    name2 = models.CharField(max_length=1024, null=True, blank=True)
    name3 = models.CharField(max_length=1024, null=True, blank=True)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.confirmed and not self.exported:
            from crm.contractors.optima_api.serializers import ContractorSerializer
            from crm.contractors.optima_api.views import ContractorObject

            serializer = ContractorSerializer(self)
            if serializer.is_valid():
                connection = ContractorObject()
                optima_id = connection.post(serializer.data)
                if optima_id:
                    self.optima_id = optima_id
                    self.code = self.tax_number
                    self.exported = True
                    super().save()
