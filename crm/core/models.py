import uuid as uuid_lib

from django.apps import apps
from django.db import models


class BaseModel(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class OptimaModel(BaseModel):
    optima_id = models.IntegerField(null=True, blank=True, unique=True)
    exported = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        try:
            return self.code
        except AttributeError:
            return super().__str__()

    def _export_to_optima(self):
        pass

    def _update_optima_obj(self):
        pass

    def _optima_synchronization(self):
        general_settings_model = apps.get_model("crm_config", "GeneralSettings")
        try:
            general_settings = general_settings_model.objects.first()
        except general_settings_model.DoesNotExist:
            general_settings = None
        if general_settings and general_settings.optima_synchronization:
            if self.exported and self.optima_id:
                self._update_optima_obj()
            elif not self.exported and not self.optima_id:
                self._export_to_optima()

    def save(self, *args, **kwargs):
        super().save()
        self._optima_synchronization()
