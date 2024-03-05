from config import celery_app
from crm.contractors.tasks import import_contractors
from crm.crm_config.tasks import import_countries, import_states
from crm.documents.tasks import import_document_types
from crm.products.tasks import import_products
from crm.service.tasks import import_attributes_definition, import_categories, import_device_types, import_stages
from crm.users.tasks import import_users
from crm.warehouses.tasks import import_warehouses


@celery_app.task
def initial_import():
    import_device_types.apply_async()
    import_categories.apply_async()
    import_stages.apply_async()
    import_attributes_definition.apply_async()
    import_products.apply_async()
    import_contractors.apply_async()
    import_document_types.apply_async()
    import_users.apply_async()
    import_warehouses.apply_async()
    import_countries.apply_async(link=import_states.s())
