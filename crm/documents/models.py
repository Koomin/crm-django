import datetime

from django.db import models

from crm.core.models import OptimaModel
from crm.warehouses.models import Warehouse


class DocumentType(OptimaModel):
    # Optima table - CDN.DokDefinicje
    symbol = models.CharField(null=False, max_length=12)
    obj_class = models.IntegerField(null=False)
    name = models.CharField(null=False, max_length=255)
    numbering_scheme = models.CharField(null=False, max_length=500)
    active = models.BooleanField(default=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, blank=True)
    to_import = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.symbol} - {self.name}"

    def format_numbering_scheme(self):
        formatted_scheme = self.numbering_scheme
        formatting_dict = {
            "@symbol": getattr(self, "symbol"),
            "@miesiac": datetime.date.today().month,
            "@rok_kal": datetime.date.today().year,
            "/@brak": "",
            "@brak/": "",
        }
        for key, value in formatting_dict.items():
            formatted_scheme = formatted_scheme.replace(key, value)
        return formatted_scheme
