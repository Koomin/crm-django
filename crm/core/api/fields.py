import base64

from rest_framework import serializers

from config.settings.base import MEDIA_ROOT


class FileBase64Field(serializers.FileField):
    def to_representation(self, value):
        if value:
            with open(f"{MEDIA_ROOT}/{value}", "rb") as pdf_file:
                return base64.b64encode(pdf_file.read())
        return None
