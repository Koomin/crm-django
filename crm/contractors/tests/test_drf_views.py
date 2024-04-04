import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from crm.contractors.models import Contractor
from crm.contractors.tests.factories import ContractorFactory
from crm.users.tests.factories import UserFactory


class TestContractorViewSet(APITestCase):
    def test_confirmed(self):
        url = reverse("api:contractor-confirmed")
        for i in range(10):
            ContractorFactory()
        self.client.force_authenticate(user=UserFactory())
        response = self.client.get(url)
        data = json.loads(response.content)
        for obj in data.get("results"):
            if obj:
                self.assertTrue(obj.get("confirmed"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Contractor.objects.filter(confirmed=True).count(), data.get("count"))

    def test_unconfirmed(self):
        url = reverse("api:contractor-unconfirmed")
        for i in range(10):
            ContractorFactory()
        self.client.force_authenticate(user=UserFactory())
        response = self.client.get(url)
        data = json.loads(response.content)
        for obj in data.get("results"):
            if obj:
                self.assertFalse(obj.get("confirmed"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Contractor.objects.filter(confirmed=False).count(), data.get("count"))
