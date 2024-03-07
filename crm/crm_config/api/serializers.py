from rest_framework import serializers

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
