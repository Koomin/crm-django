from django.core.exceptions import ValidationError
from django.test import TestCase

from crm.crm_config.models import GeneralSettings, Log
from crm.crm_config.tests.factories import GeneralSettingsFactory, LogFactory


class GeneralSettingsTest(TestCase):
    def create_general_settings(self):
        return GeneralSettingsFactory()

    def test_save(self):
        with self.assertRaises(ValidationError):
            self.create_general_settings()
        general_settings = GeneralSettings.objects.all().first()
        general_settings.optima_config_database = "TEST_DB"
        general_settings.save()
        self.assertEqual(general_settings.optima_config_database, "TEST_DB")


class LogTest(TestCase):
    def create_log(self):
        return LogFactory()

    def test_save(self):
        for i in range(0, 1000):
            log = self.create_log()
            self.assertEqual(log.number, i + 1)
        self.assertEqual(Log.objects.count(), 1000)
