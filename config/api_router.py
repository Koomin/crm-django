from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from crm.contractors.api.views import ContractorViewSet
from crm.documents.api.views import DocumentTypeViewSet
from crm.service.api.views import (
    CategoryViewSet,
    DeviceTypeViewSet,
    DeviceViewSet,
    NoteViewSet,
    ServiceOrderViewSet,
    StageViewSet,
)
from crm.users.api.views import UserViewSet
from crm.warehouses.api.views import WarehouseViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("warehouses", WarehouseViewSet)
router.register("categories", CategoryViewSet)
router.register("stages", StageViewSet)
router.register("devices-types", DeviceTypeViewSet)
router.register("devices", DeviceViewSet)
router.register("service-orders", ServiceOrderViewSet)
router.register("contractors", ContractorViewSet)
router.register("document-types", DocumentTypeViewSet)
router.register("notes", NoteViewSet)

app_name = "api"
urlpatterns = router.urls
