from config import celery_app
from crm.crm_config.models import Country, State
from crm.crm_config.optima_api.serializers import CountrySerializer, StateSerializer
from crm.crm_config.optima_api.views import CountryObject, StateObject


@celery_app.task()
def import_countries():
    country_object = CountryObject()
    objects = country_object.get()
    for obj in objects:
        serializer = CountrySerializer(obj)
        Country.objects.update_or_create(optima_id=serializer.data.get("optima_id"), defaults=serializer.data)


@celery_app.task()
def import_states():
    state_object = StateObject()
    objects = state_object.get()
    for obj in objects:
        serializer = StateSerializer(obj)
        State.objects.update_or_create(optima_id=serializer.data.get("optima_id"), defaults=serializer.data)
