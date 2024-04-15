import base64

from rest_framework import serializers

from config.settings.base import MEDIA_ROOT


class FileBase64Field(serializers.FileField):
    def to_representation(self, value):
        if value:
            try:
                with open(f"{MEDIA_ROOT}/{value}", "rb") as pdf_file:
                    return base64.b64encode(pdf_file.read())
            except FileNotFoundError as e:
                from crm.crm_config.models import Log

                Log.objects.create(
                    exception_traceback=e,
                    method_name="to_representation",
                    model_name=self.__class__.__name__,
                    object_serialized="",
                )
                return None
        return None


class FileTypeField(serializers.CharField):
    def to_representation(self, value):
        if value:
            extension = value.name.split(".")[-1]
            return extension
        return None
