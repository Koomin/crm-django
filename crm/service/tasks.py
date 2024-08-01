import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.db.utils import IntegrityError
from django.utils import timezone

from config import celery_app
from crm.crm_config.models import GeneralSettings, Log, ServiceAddress
from crm.documents.models import DocumentType
from crm.service.models import (
    Attribute,
    AttributeDefinition,
    AttributeDefinitionItem,
    Category,
    Device,
    DeviceType,
    Note,
    ServiceActivity,
    ServiceOrder,
    ServicePart,
    Stage,
)
from crm.service.optima_api.serializers import (
    AttributeDefinitionItemSerializer,
    AttributeDefinitionSerializer,
    AttributeSerializer,
    CategorySerializer,
    DeviceSerializer,
    DeviceTypeSerializer,
    NoteSerializer,
    ServiceActivitySerializer,
    ServiceOrderSerializer,
    ServicePartSerializer,
    StageSerializer,
)
from crm.service.optima_api.views import (
    AttributeDefinitionItemObject,
    AttributeDefinitionObject,
    AttributeObject,
    CategoryObject,
    DeviceObject,
    DeviceTypeObject,
    NoteObject,
    ServiceActivityObject,
    ServiceOrderObject,
    ServicePartObject,
    StageObject,
)


@celery_app.task()
def import_categories():
    category_object = CategoryObject()
    objects = category_object.get()
    for obj in objects:
        serializer = CategorySerializer(obj)
        if serializer.data:
            Category.objects.update_or_create(optima_id=serializer.data.get("optima_id"), defaults=serializer.data)


@celery_app.task()
def import_stages():
    stage_object = StageObject()
    objects = stage_object.get()
    for obj in objects:
        serializer = StageSerializer(obj)
        if serializer.data:
            Stage.objects.update_or_create(optima_id=serializer.data.get("optima_id"), defaults=serializer.data)


@celery_app.task()
def import_device_types():
    device_type_object = DeviceTypeObject()
    objects = device_type_object.get()
    for obj in objects:
        serializer = DeviceTypeSerializer(obj)
        if serializer.data:
            DeviceType.objects.update_or_create(optima_id=serializer.data.get("optima_id"), defaults=serializer.data)
    device_object = DeviceObject()
    device_objects = device_object.get()
    for dev_obj in device_objects:
        serializer = DeviceSerializer(dev_obj)
        if serializer.data:
            Device.objects.update_or_create(optima_id=serializer.data.get("optima_id"), defaults=serializer.data)


@celery_app.task()
def import_attributes_definition():
    attribute_object = AttributeDefinitionObject()
    objects = attribute_object.get()
    for obj in objects:
        serializer = AttributeDefinitionSerializer(obj)
        if serializer.data:
            AttributeDefinition.objects.update_or_create(
                optima_id=serializer.data.get("optima_id"), defaults=serializer.data
            )
    attribute_item_object = AttributeDefinitionItemObject()
    objects = attribute_item_object.get()
    for obj in objects:
        serializer = AttributeDefinitionItemSerializer(obj)
        if serializer.data:
            try:
                AttributeDefinitionItem.objects.update_or_create(
                    optima_id=serializer.data.get("optima_id"), defaults=serializer.data
                )
            except IntegrityError as e:
                Log.objects.create(
                    exception_traceback=e,
                    method_name="import_attributes_definition",
                    model_name="AttributeDefinitionItem",
                    object_serialized=serializer.data,
                )


@celery_app.task()
def update_attributes_definition():
    for obj in Attribute.objects.all().values_list("attribute_definition", flat=True).distinct():
        print(obj)


def import_service_order_full(order_objects):
    for order_obj in order_objects:
        serializer = ServiceOrderSerializer(order_obj)
        if serializer.data:
            try:
                service_order = ServiceOrder.objects.get(optima_id=serializer.data.get("optima_id"))
                for key, value in serializer.data.items():
                    setattr(service_order, key, value)
                service_order.save(with_optima_update=False)
            except ServiceOrder.DoesNotExist:
                service_order = ServiceOrder(**serializer.data)
                service_order.save(with_optima_update=False)
            service_part_object = ServicePartObject()
            part_objects = service_part_object.get(service_order.optima_id)
            if part_objects:
                for part_obj in part_objects:
                    serializer = ServicePartSerializer(part_obj)
                    if serializer.data:
                        try:
                            ServicePart.objects.update_or_create(
                                optima_id=serializer.data.get("optima_id"), defaults=serializer.data
                            )
                        except Exception as e:
                            print(e)
                            pass
            attribute_object = AttributeObject()
            attr_objects = attribute_object.get(service_order.optima_id)
            if attr_objects:
                for attr_obj in attr_objects:
                    serializer = AttributeSerializer(attr_obj)
                    if serializer.data:
                        try:
                            Attribute.objects.update_or_create(
                                optima_id=serializer.data.get("optima_id"), defaults=serializer.data
                            )
                        except IntegrityError:
                            pass
            service_activity_object = ServiceActivityObject()
            activities_objects = service_activity_object.get(service_order.optima_id)
            if activities_objects:
                for activity_obj in activities_objects:
                    serializer = ServiceActivitySerializer(activity_obj)
                    if serializer.data:
                        try:
                            ServiceActivity.objects.update_or_create(
                                optima_id=serializer.data.get("optima_id"), defaults=serializer.data
                            )
                        except Exception as e:
                            print(e)
                            pass
            note_object = NoteObject()
            note_objects = note_object.get(service_order.optima_id)
            if note_objects:
                for note_obj in note_objects:
                    serializer = NoteSerializer(note_obj)
                    if serializer.data:
                        Note.objects.update_or_create(
                            optima_id=serializer.data.get("optima_id"), defaults=serializer.data
                        )


@celery_app.task()
def full_import_orders():
    service_order_object = ServiceOrderObject()
    for document in DocumentType.objects.filter(to_import=True):
        try:
            order_objects = service_order_object.get(document.optima_id, "2024-01-01")
        except Exception as e:
            from crm.documents.api.serializers import DocumentTypeSerializer

            serializer = DocumentTypeSerializer(document)
            if serializer.is_valid():
                data = serializer.data
            else:
                data = f"document_optima_id: {document.optima_id}"
            Log.objects.create(
                exception_traceback=e,
                method_name="full_import_orders",
                model_name="ServiceOrder",
                object_serialized=data,
            )
            continue
        import_service_order_full(order_objects)


@celery_app.task()
def synchronize_order(optima_id):
    service_order_object = ServiceOrderObject()
    try:
        order_objects = service_order_object.get_by_optima_id(optima_id)
    except Exception as e:
        Log.objects.create(
            exception_traceback=e,
            method_name="synchronize_order",
            model_name="ServiceOrder",
            object_serialized=f"optima_id: {optima_id}",
        )
        return
    import_service_order_full(order_objects)


@celery_app.task()
def create_attributes(service_order_pk):
    try:
        service_order = ServiceOrder.objects.get(pk=service_order_pk)
    except Exception as e:
        Log.objects.create(
            exception_traceback=e,
            method_name="create_attributes",
            model_name="ServiceOrder",
            object_serialized=f"service_order_pk: {service_order_pk}",
        )
        return
    attributes_to_create = AttributeDefinition.objects.filter(is_active=True)
    for attribute in attributes_to_create:
        if not service_order.attributes.filter(attribute_definition=attribute).exists():
            Attribute.objects.create(
                attribute_definition=attribute, code=attribute.code, value="", service_order=service_order
            )
    return


@celery_app.task()
def email_send(service_order_pk):
    try:
        service_order = ServiceOrder.objects.get(pk=service_order_pk)
    except ServiceOrder.DoesNotExist as e:
        Log.objects.create(
            exception_traceback=e,
            method_name="email_send",
            model_name="ServiceOrder",
            object_serialized=f"service_order_pk: {service_order_pk}",
        )
        return
    current_stage = service_order.stage
    if service_order.emails_sent.filter(stage=current_stage).exists():
        return
    email_template = current_stage.email_template
    try:
        from service.models import EmailSent
    except ModuleNotFoundError:
        from crm.service.models import EmailSent
    email = EmailSent.objects.create(
        service_order=service_order,
        stage=current_stage,
        email_template=email_template,
        subject=email_template.subject,
        email=service_order.email,
    )
    if email and email.message:
        try:
            sent = send_mail(
                html_message=email.message,
                message=email.message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[
                    email.email,
                ],
                subject=email.subject,
                fail_silently=False,
            )
        except Exception as e:
            Log.objects.create(
                exception_traceback=e,
                method_name="email_send",
                model_name="EmailSent",
                object_uuid=email.uuid,
            )
        else:
            if sent:
                email.sent = sent
                email.date_of_sent = datetime.datetime.now()
                email.save()
    return


@celery_app.task()
def email_order_created():
    message = f"Nowe zgłoszenie serwisowe trafiło do systemu o godzinie {timezone.now()}."
    try:
        admin_mail = GeneralSettings.objects.first().admin_email
    except Exception as e:
        Log.objects.create(
            exception_traceback=e,
            method_name="email_order_created",
            model_name="GeneralSettings",
        )
    else:
        try:
            send_mail(
                html_message=message,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[
                    admin_mail,
                ],
                subject="Nowe zgłoszenie serwisowe",
                fail_silently=False,
            )
        except Exception as e:
            Log.objects.create(
                exception_traceback=e,
                method_name="email_order_created",
            )


@celery_app.task()
def set_service_address():
    first_service = ServiceAddress.objects.get(name="Centrala Świętochłowice")
    second_service = ServiceAddress.objects.get(name="Oddział Warszawa")
    for device in Device.objects.filter(code__startswith="PF"):
        device.available_services.set([first_service, second_service])
    for device in Device.objects.filter(code__startswith="HF"):
        device.available_services.set(first_service)
