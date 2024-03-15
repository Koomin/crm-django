import xmltodict
from django.conf import settings
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from zeep import Client


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
                serialized = {
                    "customer_city": data.get("Miejscowosc"),
                    "customer_country": "POLSKA",
                    "customer_street": f"{data.get('Ulica')} {data.get('NrNieruchomosci')}",
                    "customer_home_number": data.get("NrLokalu"),
                    "customer_postal_code": data.get("KodPocztowy"),
                    "customer_name": data.get("Nazwa"),
                }
                return Response(serialized, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)
