from rest_framework import serializers

from crm.contractors.models import Contractor


class ContractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contractor
        fields = [
            "uuid",
            "code",
            "postal_code",
            "tax_number",
            "phone_number",
            "country",
            "city",
            "street",
            "street_number",
            "home_number",
            "post",
            "state",
            "name",
            "confirmed",
        ]
