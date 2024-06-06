from django.db import models

from crm.core.models import OptimaModel


class Contractor(OptimaModel):
    code = models.CharField(max_length=120, null=True, blank=True)
    postal_code = models.CharField(max_length=20)
    tax_number = models.CharField(max_length=30)
    regon = models.CharField(max_length=20, null=True, blank=True)
    phone_number = models.CharField(max_length=30)
    country = models.CharField(max_length=250)
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

    def _split_contractor_name(self):
        if self.name:
            if len(str(self.name)) > 50:
                self.name1 = self.name[:50]
                if len(str(self.name)) > 100:
                    self.name2 = str(self.name)[51:100]
                    self.name3 = str(self.name)[100:]
                else:
                    self.name2 = str(self.name)[51:]
            else:
                self.name1 = self.name

    def _export_to_optima(self) -> (bool, str, dict):
        from crm.contractors.optima_api.serializers import ContractorSerializer
        from crm.contractors.optima_api.views import ContractorObject
        from crm.contractors.tasks import create_attributes

        serializer = ContractorSerializer(self)
        if serializer.is_valid():
            connection = ContractorObject()
            optima_id = connection.get_id_by_tax_number(self.tax_number)
            if optima_id:
                return False, "Contractor with given tax number already exists in optima.", serializer.data
            created, response = connection.post(serializer.data)
            if created and response:
                optima_id = connection.get_id_by_tax_number(self.tax_number)
                self.optima_id = optima_id
                self.exported = True
                super().save()
                create_attributes.apply_async(args=[str(self.pk)], countdown=10)
            return created, response, serializer.data
        return False, serializer.errors, {}

    def save(self, *args, **kwargs):
        self._split_contractor_name()
        if not self.code:
            self.code = self.tax_number
        super().save(*args, **kwargs)
