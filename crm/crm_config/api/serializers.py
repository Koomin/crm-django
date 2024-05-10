from django.contrib.admin.models import LogEntry
from rest_framework import serializers

from crm.crm_config.models import Country, EmailTemplate, GeneralSettings, Log, ServiceAddress, State, TaxPercentage


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["uuid", "name", "code"]


class StateSerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = State
        fields = ["uuid", "name", "country"]


class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = ["uuid", "name", "subject", "template"]


class GeneralSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralSettings
        fields = [
            "uuid",
            "optima_synchronization",
            "mailing",
            "optima_config_database",
            "optima_general_database",
            "admin_email",
        ]


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = [
            "uuid",
            "number",
            "exception_traceback",
            "method_name",
            "model_name",
            "object_uuid",
            "object_serialized",
            "created",
            "modified",
        ]


class LogEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LogEntry
        fields = ["action_time", "user", "object_id", "object_repr"]


class TaxPercentageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxPercentage
        fields = ["uuid", "name", "value"]


class ServiceAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceAddress
        fields = [
            "uuid",
            "name",
            "city",
            "country",
            "postal_code",
            "street",
            "street_number",
            "home_number",
            "phone_number",
            "email",
        ]
