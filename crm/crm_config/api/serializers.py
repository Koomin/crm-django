from rest_framework import serializers

from crm.crm_config.models import Country, State


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["uuid", "name", "code"]


class StateSerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = State
        fields = ["uuid", "name", "country"]
