from rest_framework import serializers

from crm.crm.crm_config.models import GeneralSettings
from crm.crm_config.models import Country, EmailTemplate, State


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
        fields = ["uuid", "optima_synchronization", "mailing", "optima_config_database"]
