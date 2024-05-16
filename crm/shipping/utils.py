import base64

import requests
from django.conf import settings
from django.core.files.base import ContentFile
from zeep import Client

from crm.crm_config.models import Log


class ShippingClient:
    def __init__(self):
        pass

    def _serializer(self, obj) -> dict:
        pass


class RabenClient(ShippingClient):
    def __init__(self):
        super().__init__()
        self._url = settings.RABEN_URL
        self._username = settings.RABEN_USERNAME
        self._password = settings.RABEN_PASSWORD
        self._client = Client(self._url)
        self._header = f"""
        <Security xmlns="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
                                <UsernameToken>
                                    <Username>{self._username}</Username>
                                    <Password>{self._password}</Password>
                                </UsernameToken>
                            </Security>
                        """

    def _serializer(self, obj):
        pass


class GLSClient(ShippingClient):
    def __init__(self):
        super().__init__()
        self._url = settings.GLS_URL
        self._username = settings.GLS_USERNAME
        self._password = settings.GLS_PASSWORD
        self._client = Client(self._url)
        self._session = self._login()

    def _get_credentials(self):
        return {"user_name": self._username, "user_password": self._password}

    def _login(self):
        try:
            return self._client.service.adeLogin(**self._get_credentials())
        except Exception as e:
            Log.objects.create(
                exception_traceback=e,
                method_name="login",
                model_name=self.__class__.__name__,
            )
            return None

    def _serializer(self, obj) -> dict:
        address = obj.address
        street = address.street + str(address.street_number) if address.street_number else address.street
        street = street + str(address.home_number) if address.home_number else street
        return {
            "rname1": address.name,
            # 'rname2': 'Jan (2)',
            # 'rname3': 'Kowalski (3)',
            "rcountry": address.country.code,
            "rzipcode": address.postal_code,
            "rcity": address.city,
            "rstreet": street,
            "rphone": obj.service_order.phone_number,
            "rcontact": obj.service_order.email,
            "references": "crm_service",
            "notes": "Notatka",
            "weight": 1.2,
            "quantity": 1,
            # 'srv_bool': {'cod': 1, 'cod_amount': 57},
            # 'parcels': {'items': [
            #     {'reference': 'Ref. parc01', 'weight': '1.11'},
            #     {'reference': 'Ref. parc02', 'weight': '1.22'},
            #     {'reference': 'Ref. parc03', 'weight': '1.33'}
            # ]}
        }

    def create_parcel(self, shipping_obj):
        data = {"session": self._session, "consign_prep_data": self._serializer(shipping_obj)}
        try:
            parcel_id = self._client.service.adePreparingBox_Insert(**data)
        except Exception as e:
            Log.objects.create(
                exception_traceback=e,
                method_name="create_parcel",
                model_name=self.__class__.__name__,
                object_uuid=shipping_obj.uuid,
                object_serialized=data,
            )
            return False
        else:
            shipping_obj.parcel_id = parcel_id
            shipping_obj.save_without_update()
            return True

    def create_label(self, shipping_obj):
        data = {"session": self._session, "id": shipping_obj.parcel_id, "mode": "one_label_on_a4_lt_pdf"}
        try:
            label_base64 = self._client.service.adePreparingBox_GetConsignLabels(**data)
        except Exception as e:
            Log.objects.create(
                exception_traceback=e,
                method_name="create_label",
                model_name=self.__class__.__name__,
                object_uuid=shipping_obj.uuid,
                object_serialized=data,
            )
            return False
        else:
            label = ContentFile(base64.b64decode(label_base64))
            file_name = f"{shipping_obj.parcel_id}.pdf"
            shipping_obj.label.save(file_name, label, save=True)
            return self._get_track_ids(shipping_obj)

    def _get_track_ids(self, shipping_obj):
        data = {
            "session": self._session,
            "id": shipping_obj.parcel_id,
        }
        try:
            parcel_data = self._client.service.adePreparingBox_GetConsign(**data)
        except Exception as e:
            Log.objects.create(
                exception_traceback=e,
                method_name="_get_track_ids",
                model_name=self.__class__.__name__,
                object_uuid=shipping_obj.uuid,
                object_serialized=data,
            )
            return False
        else:
            track_ids = []
            parcels = parcel_data.parcels.items
            for parcel in parcels:
                track_ids.append(parcel["number"])
            shipping_obj.track_ids = track_ids
            shipping_obj.save_without_update()
            return True

    def confirm_shipping(self, shipping_obj):
        data = {"session": self._session, "consigns_ids": [shipping_obj.parcel_id], "desc": "Potwierdzenie"}
        try:
            confirmed_id = self._client.service.adePickup_Create(**data)
        except Exception as e:
            Log.objects.create(
                exception_traceback=e,
                method_name="confirm_shipping",
                model_name=self.__class__.__name__,
                object_uuid=shipping_obj.uuid,
                object_serialized=data,
            )
            return False
        else:
            shipping_obj.confirmation_id = confirmed_id
            shipping_obj.save_without_update()
            return True

    def logout(self):
        self._client.service.adeLogout(**{"session": self._session})


class GLSTracking:
    def __init__(self, obj):
        self._tracking_numbers = obj.track_ids
        self._url = settings.GLS_TRACKING_URL

    def _get_status(self, response):
        data = response.json()
        try:
            data = data["tuStatus"][0]["progressBar"]["statusBar"]
        except Exception as e:
            Log.objects.create(
                exception_traceback=e,
                method_name="_get_current_status",
                model_name=self.__class__.__name__,
                object_serialized=data,
            )
            return None
        else:
            return data

    def _get_last_closed(self, response):
        last_completed = None
        if response.status_code == 200:
            data = self._get_status(response)
            for stage in data:
                if stage["imageStatus"] == "COMPLETE":
                    last_completed = stage["status"]
        return last_completed

    def _get_current_status(self, response):
        if response.status_code == 200:
            data = self._get_status(response)
            for stage in data:
                if stage["imageStatus"] == "CURRENT":
                    return stage["status"]
        return None

    @property
    def current_status(self):
        status = {}
        for number in self._tracking_numbers:
            response = requests.get(self._url + number)
            status[number] = self._get_current_status(response)
        return status

    @property
    def last_closed(self):
        status = {}
        for number in self._tracking_numbers:
            response = requests.get(self._url + number)
            status[number] = self._get_last_closed(response)
        return status
