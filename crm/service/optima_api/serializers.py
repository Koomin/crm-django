from django.core.exceptions import ObjectDoesNotExist

from crm.contractors.models import Contractor
from crm.core.optima import BaseOptimaSerializer
from crm.documents.models import DocumentType
from crm.service.models import (
    Attribute,
    AttributeDefinition,
    AttributeDefinitionItem,
    Category,
    Device,
    DeviceType,
    Note,
    ServiceOrder,
    Stage,
)
from crm.users.models import OptimaUser
from crm.warehouses.models import Warehouse


class CategorySerializer(BaseOptimaSerializer):
    model = Category

    def _deserialize(self) -> dict:
        return {
            "optima_id": self.obj[0],
            "code": self.obj[1],
            "code_detailed": self.obj[2],
            "description": self.obj[3],
        }


class StageSerializer(BaseOptimaSerializer):
    model = Stage

    def _deserialize(self) -> dict:
        return {"optima_id": self.obj[0], "type": self.obj[1], "code": self.obj[2], "description": self.obj[3]}


class DeviceTypeSerializer(BaseOptimaSerializer):
    model = DeviceType

    def _deserialize(self) -> dict:
        return {"optima_id": self.obj[0], "code": self.obj[1], "active": self.obj[2], "name": self.obj[3]}


class DeviceSerializer(BaseOptimaSerializer):
    model = Device

    def _get_device_type(self):
        try:
            return DeviceType.objects.get(optima_id=self.obj[4])
        except ObjectDoesNotExist:
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
    model = Note

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
            service_order = ServiceOrder.objects.get(optima_id=self.obj[6])
        except ObjectDoesNotExist:
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
    model = AttributeDefinition

    def _deserialize(self) -> dict:
        return {
            "optima_id": self.obj[0],
            "code": self.obj[1],
            "type": self.obj[2],
            "format": self.obj[3],
        }


class AttributeDefinitionItemSerializer(BaseOptimaSerializer):
    model = AttributeDefinitionItem

    def _get_attribute_definition(self):
        try:
            attribute_definition = AttributeDefinition.objects.get(optima_id=self.obj[3])
        except ObjectDoesNotExist:
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
    model = Attribute

    def _get_attribute_definition(self):
        try:
            attribute_definition = AttributeDefinition.objects.get(optima_id=self.obj[2])
        except ObjectDoesNotExist:
            return None
        else:
            return attribute_definition

    def _deserialize(self) -> dict:
        return {
            "optima_id": self.obj[0],
            "code": self.obj[1],
            "attribute_definition": self._get_attribute_definition(),
            "value": self.obj[3],
        }


class ServiceOrderSerializer(BaseOptimaSerializer):
    model = ServiceOrder

    def _get_document_type(self):
        try:
            return DocumentType.objects.get(optima_id=self.obj[1])
        except ObjectDoesNotExist:
            return None

    def _get_category(self):
        try:
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
            return Stage.objects.get(optima_id=self.obj[14])
        except ObjectDoesNotExist:
            return None

    def _get_device(self):
        try:
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
