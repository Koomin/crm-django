import datetime

from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist

from crm.contractors.models import Contractor
from crm.core.optima import BaseOptimaSerializer
from crm.documents.models import DocumentType
from crm.products.models import Product
from crm.users.models import OptimaUser
from crm.warehouses.models import Warehouse


class CategorySerializer(BaseOptimaSerializer):
    model = apps.get_model("service", "Category")

    def _deserialize(self) -> dict:
        return {
            "optima_id": self.obj[0],
            "code": self.obj[1],
            "code_detailed": self.obj[2],
            "description": self.obj[3],
        }


class StageSerializer(BaseOptimaSerializer):
    model = apps.get_model("service", "Stage")

    def _deserialize(self) -> dict:
        return {"optima_id": self.obj[0], "type": self.obj[1], "code": self.obj[2], "description": self.obj[3]}


class DeviceTypeSerializer(BaseOptimaSerializer):
    model = apps.get_model("service", "DeviceType")

    def _deserialize(self) -> dict:
        return {"optima_id": self.obj[0], "code": self.obj[1], "active": self.obj[2], "name": self.obj[3]}


class DeviceSerializer(BaseOptimaSerializer):
    model = apps.get_model("service", "Device")

    def _get_device_type(self):
        try:
            DeviceType = apps.get_model("service", "DeviceType")
            return DeviceType.objects.get(optima_id=self.obj[4])
        except ObjectDoesNotExist:
            self._valid = False
            return None

    def _deserialize(self) -> dict:
        return {
            "optima_id": self.obj[0],
            "code": self.obj[1],
            "name": self.obj[2],
            "description": self.obj[3],
            "device_type": self._get_device_type(),
        }


class NoteSerializer(BaseOptimaSerializer):
    model = apps.get_model("service", "Note")

    def _get_user(self):
        try:
            optima_user = OptimaUser.objects.get(optima_id=self.obj[3])
        except ObjectDoesNotExist:
            return None
        else:
            try:
                user = optima_user.user
                return user
            except Exception:
                return None

    def _get_service_order(self):
        try:
            ServiceOrder = apps.get_model("service", "ServiceOrder")
            service_order = ServiceOrder.objects.get(optima_id=self.obj[6])
        except ObjectDoesNotExist:
            self._valid = False
            return None
        else:
            return service_order

    def _deserialize(self) -> dict:
        return {
            "optima_id": self.obj[0],
            "number": self.obj[1],
            "date": self.obj[4],
            "description": self.obj[5],
            "user": self._get_user(),
            "service_order": self._get_service_order(),
        }


class AttributeDefinitionSerializer(BaseOptimaSerializer):
    model = apps.get_model("service", "AttributeDefinition")

    def _deserialize(self) -> dict:
        return {
            "optima_id": self.obj[0],
            "code": self.obj[1],
            "type": self.obj[2],
            "format": self.obj[3],
        }


class AttributeDefinitionItemSerializer(BaseOptimaSerializer):
    model = apps.get_model("service", "AttributeDefinitionItem")

    def _get_attribute_definition(self):
        try:
            attribute_definition = self.model.objects.get(optima_id=self.obj[3])
        except ObjectDoesNotExist:
            self._valid = False
            return None
        else:
            return attribute_definition

    def _deserialize(self) -> dict:
        return {
            "optima_id": self.obj[0],
            "value": self.obj[1],
            "number": self.obj[2],
            "attribute_definition": self._get_attribute_definition(),
        }


class AttributeSerializer(BaseOptimaSerializer):
    model = apps.get_model("service", "Attribute")

    def _get_attribute_definition(self):
        try:
            attribute_definition = self.model.objects.get(optima_id=self.obj[2])
        except ObjectDoesNotExist:
            self._valid = False
            return None
        else:
            return attribute_definition

    def _get_service_order(self):
        try:
            service_order = self.model.objects.get(optima_id=self.obj[4])
        except ObjectDoesNotExist:
            self._valid = False
            return None
        else:
            return service_order

    def _get_format(self):
        return int(self.obj[5])

    def _get_value(self):
        if self._get_format() == 4 and self.obj[3]:
            return datetime.datetime(year=1800, month=12, day=28).date() + datetime.timedelta(days=int(self.obj[3]))
        return self.obj[3]

    def _deserialize(self) -> dict:
        return {
            "optima_id": self.obj[0],
            "code": self.obj[1],
            "attribute_definition": self._get_attribute_definition(),
            "value": self._get_value(),
            "service_order": self._get_service_order(),
        }


class ServicePartSerializer(BaseOptimaSerializer):
    model = apps.get_model("service", "ServicePart")

    def _get_product(self):
        try:
            return Product.objects.get(optima_id=self.obj[2])
        except Product.DoesNotExist:
            self._valid = False
            return None

    def _get_warehouse(self):
        try:
            return Warehouse.objects.get(optima_id=self.obj[5])
        except Warehouse.DoesNotExist:
            self._valid = False
            return None

    def _get_user(self):
        try:
            return OptimaUser.objects.get(optima_id=self.obj[4])
        except OptimaUser.DoesNotExist:
            self._valid = False
            return None

    def _get_service_order(self):
        try:
            ServiceOrder = apps.get_model("service", "ServiceOrder")
            return ServiceOrder.objects.get(optima_id=self.obj[16])
        except ServiceOrder.DoesNotExist:
            self._valid = False
            return None

    def _deserialize(self) -> dict:
        return {
            "optima_id": self.obj[0],
            "number": self.obj[1],
            "product": self._get_product(),
            "to_return": self.obj[3],
            "user": self._get_user(),
            "warehouse": self._get_warehouse(),
            "status_collected": self.obj[6],
            "document": self.obj[7],
            "to_invoicing": self.obj[8],
            "price_net": self.obj[9],
            "price_gross": self.obj[10],
            "price_discount": self.obj[11],
            "quantity": self.obj[12],
            "quantity_collected": self.obj[13],
            "quantity_released": self.obj[14],
            "unit": self.obj[15],
            "service_order": self._get_service_order(),
        }


class ServiceActivitySerializer(BaseOptimaSerializer):
    model = apps.get_model("service", "ServiceActivity")

    def _get_product(self):
        try:
            return Product.objects.get(optima_id=self.obj[3])
        except Product.DoesNotExist:
            self._valid = False
            return None

    def _get_user(self):
        try:
            return OptimaUser.objects.get(optima_id=self.obj[4])
        except OptimaUser.DoesNotExist:
            self._valid = False
            return None

    def _get_service_order(self):
        try:
            ServiceOrder = apps.get_model("service", "ServiceOrder")
            return ServiceOrder.objects.get(optima_id=self.obj[1])
        except ServiceOrder.DoesNotExist:
            self._valid = False
            return None

    def _deserialize(self) -> dict:
        return {
            "optima_id": self.obj[0],
            "service_order": self._get_service_order(),
            "number": self.obj[2],
            "product": self._get_product(),
            "user": self._get_user(),
            "is_finished": self.obj[5],
            "to_invoicing": self.obj[6],
            "date_of_service": self.obj[7],
            "date_from": self.obj[8],
            "date_to": self.obj[9],
            "price_discount": self.obj[10],
            "price_net": self.obj[11],
            "price_gross": self.obj[12],
            "quantity": self.obj[13],
            "value_net": self.obj[14],
            "value_gross": self.obj[15],
            "unit": self.obj[16],
        }


class ServiceOrderSerializer(BaseOptimaSerializer):
    model = apps.get_model("service", "ServiceOrder")

    def _get_document_type(self):
        try:
            return DocumentType.objects.get(optima_id=self.obj[1])
        except ObjectDoesNotExist:
            return None

    def _get_category(self):
        try:
            Category = apps.get_model("service", "Category")
            return Category.objects.get(optima_id=self.obj[2])
        except ObjectDoesNotExist:
            return None

    def _get_status(self):
        return self.obj[5]

    def _get_contractor(self):
        try:
            return Contractor.objects.get(optima_id=self.obj[7])
        except ObjectDoesNotExist:
            return None

    def _get_user(self):
        try:
            optima_user = OptimaUser.objects.get(optima_id=self.obj[8])
        except ObjectDoesNotExist:
            return None
        else:
            try:
                user = optima_user.user
                return user
            except Exception:
                return None

    def _get_warehouse(self):
        try:
            return Warehouse.objects.get(optima_id=self.obj[13])
        except ObjectDoesNotExist:
            return None

    def _get_stage(self):
        try:
            Stage = apps.get_model("service", "Stage")
            return Stage.objects.get(optima_id=self.obj[14])
        except ObjectDoesNotExist:
            return None

    def _get_device(self):
        try:
            Device = apps.get_model("service", "Device")
            return Device.objects.get(optima_id=self.obj[18])
        except ObjectDoesNotExist:
            return None

    def _get_name(self):
        return (self.obj[24] + " " + self.obj[25] + " " + self.obj[26]).strip()

    def _get_home_number(self):
        try:
            _home_number = int(self.obj[28])
        except ValueError:
            return None
        else:
            return _home_number

    def _serialize_document_type(self):
        try:
            return self.obj.document_type.optima_id
        except AttributeError:
            self._valid = False
            return None

    def _serialize_category(self):
        try:
            return self.obj.category.optima_id
        except AttributeError:
            self._valid = False
            return None

    def _serialize_contractor(self):
        try:
            return self.obj.contractor.optima_id
        except AttributeError:
            self._valid = False
            return None

    def _serialize_user(self):
        try:
            return self.obj.user.optima_user.optima_id
        except AttributeError:
            self._valid = False
            return None

    def _serialize_user_code(self):
        try:
            return self.obj.user.optima_user.code
        except AttributeError:
            self._valid = False
            return None

    def _serialize_user_name(self):
        try:
            return self.obj.user.optima_user.name
        except AttributeError:
            self._valid = False
            return None

    def _serialize_warehouse(self):
        try:
            return self.obj.warehouse.optima_id
        except AttributeError:
            self._valid = False
            return None

    def _serialize_stage(self):
        try:
            return self.obj.stage.optima_id
        except AttributeError:
            self._valid = False
            return None

    def _serialize_device(self):
        try:
            return self.obj.device.optima_id
        except AttributeError:
            self._valid = False
            return None

    def _serialize_bufor(self):
        return 1 if self.obj.status else 0

    def _deserialize(self) -> dict:
        return {
            "optima_id": self.obj[0],
            "document_type": self._get_document_type(),
            "category": self._get_category(),
            "number_scheme": self.obj[3],
            "number": self.obj[4],
            "status": self._get_status(),
            "state": self.obj[6],
            "contractor": self._get_contractor(),
            "user": self._get_user(),
            "document_date": self.obj[9],
            "acceptance_date": self.obj[10],
            "realization_date": self.obj[11],
            "closing_date": self.obj[12],
            "warehouse": self._get_warehouse(),
            "stage": self._get_stage(),
            "net_value": self.obj[15],
            "gross_value": self.obj[16],
            "description": self.obj[17],
            "device": self._get_device(),
            "full_number": self.obj[19],
            "email": self.obj[20],
            "phone_number": self.obj[21],
            "contractor_country": self.obj[22],
            "contractor_city": self.obj[23],
            "contractor_name1": self.obj[24],
            "contractor_name2": self.obj[25],
            "contractor_name3": self.obj[26],
            "contractor_street_number": self.obj[27],
            "contractor_home_number": self._get_home_number(),
            "contractor_post": self.obj[29],
            "contractor_street": self.obj[30],
            "contractor_state": self.obj[31],
            "contractor_type": self.obj[32],
            "contractor_postal_code": self.obj[33],
            "contractor_name": self._get_name(),
        }

    def _serialize(self):
        return {
            "SrZ_DDfId": self._serialize_document_type(),
            "SrZ_KatID": self._serialize_category(),
            "SrZ_NumerString": self.obj.number_scheme,
            "SrZ_NumerNr": self.obj.number,
            "SrZ_Bufor": self._serialize_bufor(),
            "SrZ_Stan": self.obj.state,
            "SrZ_PodmiotId": self._serialize_contractor(),
            "SrZ_OdbId": self._serialize_contractor(),
            "SrZ_OpeZalId": self._serialize_user(),
            "SrZ_DataDok": self.obj.document_date,
            "SrZ_DataPrzyjecia": self.obj.acceptance_date,
            "SrZ_DataRealizacji": self.obj.realization_date,
            "SrZ_DataZamkniecia": self.obj.closing_date,
            "SrZ_MagId": self._serialize_warehouse(),
            "SrZ_EtapId": self._serialize_stage(),
            "SrZ_WartoscNetto": self.obj.net_value,
            "SrZ_WartoscNettoPLN": self.obj.net_value,
            "SrZ_WartoscBrutto": self.obj.gross_value,
            "SrZ_WartoscBruttoPLN": self.obj.gross_value,
            "SrZ_WartoscNettoDoFA": self.obj.net_value,
            "SrZ_WartoscNettoDoFAPLN": self.obj.net_value,
            "SrZ_WartoscBruttoDoFA": self.obj.gross_value,
            "SrZ_WartoscBruttoDoFAPLN": self.obj.gross_value,
            "SrZ_Opis": self.obj.description,
            "SrZ_SrUId": self._serialize_device(),
            # "SrZ_NumerPelny": self.obj.full_number,
            "SrZ_Email": self.obj.email,
            "SrZ_Telefon": self.obj.phone_number,
            "SrZ_PodKraj": self.obj.contractor_country,
            "SrZ_PodMiasto": self.obj.contractor_city,
            "SrZ_PodNazwa1": self.obj.contractor_name1,
            "SrZ_PodNazwa2": self.obj.contractor_name2,
            "SrZ_PodNazwa3": self.obj.contractor_name3,
            "SrZ_PodNrDomu": self.obj.contractor_street_number,
            "SrZ_PodNrLokalu": self.obj.contractor_home_number,
            "SrZ_PodPoczta": self.obj.contractor_post,
            "SrZ_PodUlica": self.obj.contractor_street,
            "SrZ_PodWojewodztwo": self.obj.contractor_state,
            "SrZ_PodmiotTyp": self.obj.contractor_type,
            "SrZ_PodKodPocztowy": self.obj.contractor_postal_code,
            "SrZ_OdbKraj": self.obj.contractor_country,
            "SrZ_OdbMiasto": self.obj.contractor_city,
            "SrZ_OdbNazwa1": self.obj.contractor_name1,
            "SrZ_OdbNazwa2": self.obj.contractor_name2,
            "SrZ_OdbNazwa3": self.obj.contractor_name3,
            "SrZ_OdbNrDomu": self.obj.contractor_street_number,
            "SrZ_OdbNrLokalu": self.obj.contractor_home_number,
            "SrZ_OdbPoczta": self.obj.contractor_post,
            "SrZ_OdbUlica": self.obj.contractor_street,
            "SrZ_OdbWojewodztwo": self.obj.contractor_state,
            "SrZ_OdbiorcaTyp": self.obj.contractor_type,
            "SrZ_OdbKodPocztowy": self.obj.contractor_postal_code,
            "SrZ_OpeModKod": self._serialize_user_code(),
            "SrZ_OpeModNazwisko": self._serialize_user_name(),
            "SrZ_OpeZalKod": self._serialize_user_code(),
            "SrZ_OpeZalNazwisko": self._serialize_user_name(),
        }

    @property
    def _default_db_values(self) -> dict:
        return {
            "SrZ_Priorytet": 1,
            "SrZ_Wykonano": "0.00",
            "SrZ_TypNB": 1,
            "SrZ_CzasRealizacjiCzynnosci": 0,
            "SrZ_ZbiorczeFaCzesci": 0,
            "SrZ_ZbiorczeFaCzynnosci": 0,
            "SrZ_TS_Zal": datetime.datetime.now(),
            "SrZ_TS_Mod": datetime.datetime.now(),
            "SrZ_DokStatus": " ",
            "SrZ_OdbAdres2": " ",
            "SrZ_PodAdres2": " ",
            "SrZ_PodGmina": " ",
            "SrZ_OdbGmina": " ",
            "SrZ_PodPowiat": " ",
            "SrZ_OdbPowiat": " ",
            "SrZ_ZlecajacyNazwisko": " ",
            "SrZ_Waluta": " ",
            "SrZ_KursNumer": 3,
            "SrZ_KursL": 1.0000,
            "SrZ_KursM": 1,
            "SrZ_DataKur": datetime.datetime(year=1900, month=1, day=1, hour=0, minute=0, second=0, microsecond=0),
            "SrZ_FplTyp": 0,
            "SrZ_TerminPlatTyp": 0,
            "SrZ_PodmiotTyp": 1,  # sprawdzic czy zawsze 1
            "SrZ_OdbiorcaTyp": 1,  # sprawdzic czy zawsze 1
        }
