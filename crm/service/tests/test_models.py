import datetime

from django.test import TestCase

from crm.service.models import Stage
from crm.service.tests.factories import ServiceActivityFactory, StageFactory


class StageTest(TestCase):
    def create_stage(self):
        return StageFactory()

    def test_save(self):
        stage = None
        for i in range(0, 4):
            stage = self.create_stage()
            stage.is_default = True
            stage.save()
            self.assertTrue(stage.is_default)
        if stage:
            for current_stage in Stage.objects.all():
                if current_stage != stage:
                    self.assertFalse(current_stage.is_default)
                else:
                    self.assertTrue(current_stage.is_default)


class ServiceActivityTest(TestCase):
    def create_service(self):
        return ServiceActivityFactory()

    def create_service_empty(self):
        return ServiceActivityFactory(date_from=None, date_to=None)

    def test_save(self):
        service_activity = self.create_service()
        self.assertIsNotNone(service_activity.date_from)
        self.assertIsNotNone(service_activity.date_to)
        self.assertIsInstance(service_activity.date_from, datetime.datetime)
        self.assertIsInstance(service_activity.date_to, datetime.datetime)

    def test_save_without_dates(self):
        service_activity = self.create_service_empty()
        self.assertIsNotNone(service_activity.date_from)
        self.assertIsNotNone(service_activity.date_to)
        self.assertIsInstance(service_activity.date_from, datetime.datetime)
        self.assertIsInstance(service_activity.date_to, datetime.datetime)
        self.assertEqual(service_activity.date_from, service_activity.date_to)
