import base64

import requests
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils import timezone
from zeep import Client
from zeep.wsse import UsernameToken

from crm.crm_config.models import Log


class ShippingClient:
    def __init__(self):
        pass

    def _serializer(self, obj) -> dict:
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
            "references": "crm_service",
            "notes": f"{obj.service_order.device.name}, Prośba o kontakt z klientem.",
            "rname1": "",
            "rcountry": "",
            "rzipcode": "",
            "rcity": "",
            "rstreet": "",
            "rphone": "",
            "rcontact": "",
            "weight": 0.01,
            "srv_bool": {"pr": 1},
            "srv_ppe": {
                "sname1": address.name,
                # 'rname2': 'Jan (2)',
                # 'rname3': 'Kowalski (3)',
                "scountry": address.country.code,
                "szipcode": address.postal_code,
                "scity": address.city,
                "sstreet": street,
                "sphone": obj.service_order.phone_number,
                "scontact": obj.service_order.email,
                "rname1": "",
                "rcountry": "",
                "rzipcode": "",
                "rcity": "",
                "rstreet": "",
                "rphone": "",
                "rcontact": "",
                "weight": 0.01,
            },
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
            return self._get_track_ids(shipping_obj)

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
            # _get_track_ids moved to create_parcel while create_label method is unnecessary
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


class RabenClient:
    def __init__(self):
        self._url = settings.RABEN_URL
        self._username = settings.RABEN_USERNAME
        self._password = settings.RABEN_PASSWORD
        self._client = self._login()

    def _login(self):
        try:
            return Client(self._url, wsse=UsernameToken(self._username, self._password))
        except Exception as e:
            Log.objects.create(
                exception_traceback=e,
                method_name="login",
                model_name=self.__class__.__name__,
            )
            return None

    def _header(self):
        return {
            "HeaderVersion": "1",
            "Sender": {
                "Identifier": "WAGNESWIIM",
            },
            "Receiver": {
                "Identifier": "Raben Poland Test",
            },
            "DocumentIdentification": {
                "Standard": "GS1",
                "Type": "Transport Instruction",
                "InstanceIdentifier": "100002",
                "TypeVersion": "3.2",
                "CreationDateAndTime": str(timezone.now()),
            },
            "BusinessScope": {
                "Scope": [
                    {"Type": "EDIcustomerNumber", "InstanceIdentifier": "90000050"},
                    {"Type": "fileType", "InstanceIdentifier": "NF"},
                    {"Type": "department", "InstanceIdentifier": 63},
                    {"Type": "application", "InstanceIdentifier": "INT"},
                ]
            },
        }

    def _serializer(self, obj, parcel_id) -> dict:
        address = obj.address
        street = address.street + str(address.street_number) if address.street_number else address.street
        street = street + str(address.home_number) if address.home_number else street
        return {
            "creationDateTime": str(timezone.now()),
            "documentStatusCode": "ORIGINAL",
            "documentActionCode": "ADD",
            "transportInstructionIdentification": {"entityIdentification": 1},
            "transportInstructionFunction": "SHIPMENT",
            "logisticServicesBuyer": {
                "additionalPartyIdentification": {
                    "additionalPartyIdentificationTypeCode": "searchname",
                    "_value_1": "WAGNESWIIM",
                },
            },
            "transportInstructionShipment": {
                "additionalShipmentIdentification": {
                    "additionalShipmentIdentificationTypeCode": "refopd",
                    "_value_1": f"{parcel_id}",
                },
                "receiver": {
                    "additionalPartyIdentification": {
                        "additionalPartyIdentificationTypeCode": "searchname",
                        "_value_1": "WAGNESWIIM",
                    },
                    "address": {
                        "city": "Świętochłowice",
                        "countryCode": "PL",
                        "name": "Wagner Service",
                        "postalCode": "41-100",
                        "streetAddressOne": "E.Imieli 18",
                    },
                },
                "shipper": {
                    "additionalPartyIdentification": {
                        "additionalPartyIdentificationTypeCode": "searchname",
                        "_value_1": obj.service_order.contractor_name,
                    },
                    "address": {
                        "city": address.city,
                        "countryCode": address.country.code,
                        "name": address.name,
                        "postalCode": address.postal_code,
                        "streetAddressOne": street,
                    },
                },
                "shipTo": {
                    "additionalPartyIdentification": {
                        "additionalPartyIdentificationTypeCode": "searchname",
                        "_value_1": "WAGNESWIIM",
                    },
                    "address": {
                        "city": "Świętochłowice",
                        "countryCode": "PL",
                        "name": "Wagner Service",
                        "postalCode": "41-100",
                        "streetAddressOne": "E.Imieli 18",
                    },
                    "contact": {
                        "contactTypeCode": "BJ",
                        "personName": "ImieNazwisko",
                        "communicationChannel": {
                            "communicationChannelCode": "EMAIL",
                            "communicationValue": "email@email.pl",
                        },
                    },
                },
                "shipFrom": {
                    "address": {
                        "city": address.city,
                        "countryCode": address.country.code,
                        "name": address.name,
                        "postalCode": address.postal_code,
                        "streetAddressOne": street,
                    },
                    "contact": {
                        "contactTypeCode": "BJ",
                        "personName": "",
                        "communicationChannel": [
                            {
                                "communicationChannelCode": "EMAIL",
                                "communicationValue": obj.service_order.email,
                            },
                            {
                                "communicationChannelCode": "TELEPHONE",
                                "communicationValue": obj.service_order.phone_number,
                            },
                        ],
                    },
                },
                "transportInstructionTerms": {
                    "transportServiceCategoryType": "30",
                },
                # 'plannedDelivery': {
                #     'logisticEventPeriod': {
                #         'beginDate': '',
                #         'endDate': '',
                #         'beginTime': '',
                #         'endTime': ''
                #     }
                # },
                "plannedDespatch": {
                    "logisticEventPeriod": {
                        "beginDate": "",
                        "endDate": "",
                        "beginTime": "08:00:00",
                        "endTime": "16:00:00",
                    }
                },
                "transportInstructionShipmentItem": {
                    "lineItemNumber": "1",
                    "parentLineItemNumber": "1",
                    "logisticUnit": {
                        "grossWeight": {"_value_1": "23", "measurementUnitCode": "KGM"},
                        "dimension": {
                            "depth": {"_value_1": "1.2", "measurementUnitCode": "MTR"},
                            "height": {"_value_1": "0.6", "measurementUnitCode": "MTR"},
                            "width": {"_value_1": "0.6", "measurementUnitCode": "MTR"},
                        },
                    },
                    "transportCargoCharacteristics": {
                        # ds/ep
                        "cargoTypeCode": "neam",
                        "cargoTypeDescription": {"languageCode": "PL", "_value_1": "Produkty ."},
                        "totalPackageQuantity": {
                            "_value_1": "1",
                            "measurementUnitCode": "ds",
                        },
                        "totalGrossVolume": {"measurementUnitCode": "MTQ", "_value_1": 2.112},
                        "totalGrossWeight": {"measurementUnitCode": "KGM", "_value_1": 23.00},
                        "totalLoadingLength": {"measurementUnitCode": "PP", "_value_1": 1.00},
                        "totalItemQuantity": {"measurementUnitCode": "ds", "_value_1": 1.00},
                    },
                },
            },
        }

    def create_parcel(self, shipping_obj):
        parcel_id = f"{shipping_obj.service_order.contractor.id}{shipping_obj.id}"
        data = self._serializer(shipping_obj, parcel_id=parcel_id)
        try:
            response = self._client.service.importTransportInstruction(self._header(), transportInstruction=data)
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
            return self._get_track_ids(shipping_obj, response)

    def create_label(self, shipping_obj):
        data = {
            "transportDocumentRequest": {
                "creationDateTime": str(timezone.now()),
                "documentStatusCode": "ADDITIONAL_TRANSMISSION",
                "documentActionCode": "GET_DOC_PDF",
                "transportDocumentRequestIdentification": {
                    "entityIdentification": 1,
                    "contentOwner": {
                        "additionalPartyIdentification": {
                            "additionalPartyIdentificationTypeCode": "searchname",
                            "_value_1": "WAGNESWIIM",
                        }
                    },
                },
                "transportDocumentInformationCode": "LABELS",
                "transportDocumentObjectCode": "INLINE",
                "transportDocumentRequestShipment": {
                    "additionalShipmentIdentification": {
                        "additionalShipmentIdentificationTypeCode": "refopd",
                        "_value_1": f"{shipping_obj.parcel_id}",
                    }
                },
            }
        }

        try:
            with self._client.settings(raw_response=True):
                response = self._client.service.getTransportDocument(self._header(), transportDocumentRequest=data)
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
            import xml.etree.ElementTree as ET

            root = ET.fromstring(response.text)
            label_base64 = root.find(".//transportDocumentObjectAttachment").text
            label = ContentFile(base64.b64decode(label_base64))
            file_name = f"{shipping_obj.parcel_id}.pdf"
            shipping_obj.label.save(file_name, label, save=True)
            # _get_track_ids moved to create_parcel while create_label method is unnecessary
            return True

    def _get_track_ids(self, shipping_obj, response):
        transport_instruction = response.transportInstructionResponse[0].transportInstructionShipment[0]
        self.track_id = transport_instruction.additionalShipmentIdentification[1]._value_1
        if self.track_id:
            shipping_obj.track_ids = [
                self.track_id,
            ]
            shipping_obj.save_without_update()

    def logout(self):
        return True

    def confirm_shipping(self):
        if self.track_id:
            return True
        return False
