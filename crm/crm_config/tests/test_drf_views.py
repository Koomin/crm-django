import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from crm.crm_config.api.serializers import GeneralSettingsSerializer
from crm.crm_config.models import GeneralSettings
from crm.users.tests.factories import UserFactory


class TestGeneralSettingsViewSet(APITestCase):
    def get_all(self):
        return GeneralSettings.objects.all()

    def test_list(self):
        general_settings_all = self.get_all()
        general_settings = general_settings_all.first()
        serializer = GeneralSettingsSerializer(general_settings)
        url = reverse("api:generalsettings-list")
        self.client.force_authenticate(user=UserFactory())
        response = self.client.get(url)
        data = json.loads(response.content)
        self.assertEqual(general_settings_all.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("uuid"), str(general_settings.uuid))
        self.assertEqual(data, serializer.data)
