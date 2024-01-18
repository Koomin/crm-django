from django.contrib.auth import get_user_model

from config import celery_app
from crm.users.models import OptimaUser
from crm.users.optima_api.serializers import UserOptimaSerializer
from crm.users.optima_api.views import UserObject

User = get_user_model()


@celery_app.task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return User.objects.count()


@celery_app.task()
def import_users():
    user_object = UserObject()
    users = user_object.get()
    for obj in users:
        serializer = UserOptimaSerializer(obj)
        OptimaUser.objects.update_or_create(optima_id=serializer.data.get("optima_id"), defaults=serializer.data)
