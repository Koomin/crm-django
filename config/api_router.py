from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from crm.contractors.api.views import ContractorViewSet
from crm.crm_config.api.views import (
    CountryViewSet,
    EmailTemplateViewSet,
    GeneralSettingsViewSet,
    LogEntryViewSet,
    LogViewSet,
    ServiceAddressViewSet,
    StateViewSet,
    TaxPercentageViewSet,
)
from crm.documents.api.views import DocumentTypeViewSet
from crm.products.api.views import ProductViewSet
from crm.service.api.views import (
    AttributeDefinitionItemViewSet,
    AttributeDefinitionViewSet,
    AttributeViewSet,
    CategoryViewSet,
    DeviceCatalogViewSet,
    DeviceTypeViewSet,
    DeviceViewSet,
    EmailSentViewSet,
    NewServiceOrderViewSet,
    NoteViewSet,
    OrderTypeViewSet,
    PurchaseDocumentViewSet,
    ServiceActivityViewSet,
    ServiceOrderViewSet,
    StageDurationViewSet,
    StageViewSet,
)
from crm.shipping.api.views import (
    ShippingAddressViewSet,
    ShippingCompanyViewSet,
    ShippingMethodViewSet,
    ShippingStatusViewSet,
    ShippingViewSet,
    StatusViewSet,
)
from crm.users.api.views import OptimaUserViewSet, UserViewSet
from crm.warehouses.api.views import WarehouseViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("optima-users", OptimaUserViewSet)
router.register("warehouses", WarehouseViewSet)
router.register("categories", CategoryViewSet)
router.register("stages", StageViewSet)
router.register("devices-types", DeviceTypeViewSet)
router.register("devices", DeviceViewSet)
router.register("devices-catalogs", DeviceCatalogViewSet)
router.register("service-orders", ServiceOrderViewSet)
router.register("purchase-document", PurchaseDocumentViewSet, basename="purchasedocument")
router.register("new-service-orders", NewServiceOrderViewSet, basename="newserviceorder")
router.register("contractors", ContractorViewSet)
router.register("document-types", DocumentTypeViewSet)
router.register("notes", NoteViewSet)
router.register("order-types", OrderTypeViewSet)
router.register("states", StateViewSet)
router.register("countries", CountryViewSet)
router.register("attributes", AttributeViewSet)
router.register("attributes-definition", AttributeDefinitionViewSet)
router.register("attributes-definition-items", AttributeDefinitionItemViewSet)
router.register("stage-durations", StageDurationViewSet)
router.register("service-activities", ServiceActivityViewSet)
router.register("products", ProductViewSet)
router.register("email-templates", EmailTemplateViewSet)
router.register("general-settings", GeneralSettingsViewSet)
router.register("logs", LogViewSet)
router.register("log-entries", LogEntryViewSet)
router.register("emails-sent", EmailSentViewSet)
router.register("shipping", ShippingViewSet)
router.register("shipping-addresses", ShippingAddressViewSet)
router.register("shipping-statuses", ShippingStatusViewSet)
router.register("statuses", StatusViewSet)
router.register("taxes", TaxPercentageViewSet)
router.register("shipping-companies", ShippingCompanyViewSet)
router.register("shipping-methods", ShippingMethodViewSet)
router.register("service-address", ServiceAddressViewSet)

app_name = "api"
urlpatterns = router.urls
