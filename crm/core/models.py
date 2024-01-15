import uuid as uuid_lib

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
            return self.name
        except AttributeError:
            return super().__str__()
