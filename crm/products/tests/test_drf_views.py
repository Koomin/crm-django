import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from crm.products.models import Product
from crm.products.tests.factories import ProductFactory
from crm.users.tests.factories import UserFactory


class TestProductsViewSet(APITestCase):
    def setUp(self):
        self.client.force_authenticate(user=UserFactory())
        for i in range(100):
            ProductFactory()

    def test_services(self):
        url = reverse("api:product-services")
        response = self.client.get(url)
        data = json.loads(response.content)
        for obj in data:
            if obj:
                self.assertEqual(obj.get("type"), Product.ProductType.SERVICE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.filter(type=Product.ProductType.SERVICE).count(), len(data))

    def test_products(self):
        url = reverse("api:product-products")
        response = self.client.get(url)
        data = json.loads(response.content)
        for obj in data:
            if obj:
                self.assertEqual(obj.get("type"), Product.ProductType.PRODUCT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.filter(type=Product.ProductType.PRODUCT).count(), len(data))
