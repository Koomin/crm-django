import xmltodict
from django.conf import settings
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from zeep import Client

from crm.crm_config.api.serializers import CountrySerializer, StateSerializer
from crm.crm_config.models import Country, State


@api_view(http_method_names=["GET"])
@permission_classes(
    [
        AllowAny,
    ]
)
@authentication_classes(
    [
        BasicAuthentication,
    ]
)
def gus_data_by_tax_id(request, tax_id):
    url = settings.BIR_ENDPOINT
    api_key = settings.BIR_API_KEY
    client_bir = Client(url)
    sid = client_bir.service.Zaloguj(pKluczUzytkownika=api_key)
    if sid:
        with client_bir.settings(extra_http_headers={"sid": sid}):
            response = client_bir.service.DaneSzukajPodmioty(pParametryWyszukiwania={"Nip": tax_id})
            data = xmltodict.parse(response)
            if data:
                data = data.get("root").get("dane")
                state = data.get("Wojewodztwo")
                country = "POLSKA"
                try:
                    state_obj = State.objects.get(name=state)
                except State.DoesNotExist:
                    state_obj = ""
                else:
                    state_obj = StateSerializer(state_obj).data
                try:
                    country_obj = Country.objects.get(name=country)
                except Country.DoesNotExist:
                    country_obj = ""
                else:
                    country_obj = CountrySerializer(country_obj).data
                if name := data.get("Nazwa"):
                    serialized = {
                        "contractor_city": data.get("Miejscowosc"),
                        "contractor_country_obj": country_obj,
                        "contractor_country": country_obj.get("uuid"),
                        "contractor_country_name": country,
                        "contractor_street": f"{data.get('Ulica')}",
                        "contractor_street_number": f"{data.get('NrNieruchomosci')}",
                        "contractor_home_number": data.get("NrLokalu"),
                        "contractor_postal_code": data.get("KodPocztowy"),
                        "contractor_name": name,
                        "contractor_state_obj": state_obj,
                        "contractor_state": state,
                        "contractor_regon": data.get("Regon"),
                    }
                    return Response(serialized, status=status.HTTP_200_OK)
    return Response({}, status=status.HTTP_404_NOT_FOUND)
