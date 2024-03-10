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

    def _export_to_optima(self) -> (bool, str, dict):
        pass

    def _update_optima_obj(self) -> (bool, str, dict):
        pass

    def _optima_synchronization(self):
        general_settings_model = apps.get_model("crm_config", "GeneralSettings")
        try:
            general_settings = general_settings_model.objects.first()
        except general_settings_model.DoesNotExist:
            general_settings = None
        if general_settings and general_settings.optima_synchronization:
            from crm.crm_config.models import Log

            if self.exported and self.optima_id:
                updated, response, data = self._update_optima_obj()
                if not updated:
                    Log.objects.create(
                        exception_traceback=response,
                        method_name=self.__class__.__name__,
                        model_name=self.__class__.__name__,
                        object_uuid=self.uuid,
                        object_serialized=data,
                    )
            elif not self.exported and not self.optima_id:
                created, response, data = self._export_to_optima()
                if not created:
                    Log.objects.create(
                        exception_traceback=response,
                        method_name=self.__class__.__name__,
                        model_name=self.__class__.__name__,
                        object_uuid=self.uuid,
                        object_serialized=data,
                    )

    def save(self, *args, **kwargs):
        super().save()
        self._optima_synchronization()
