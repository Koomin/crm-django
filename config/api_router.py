from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from crm.users.api.views import UserViewSet
from crm.warehouses.api.views import WarehouseViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("warehouses", WarehouseViewSet)

app_name = "api"
urlpatterns = router.urls
