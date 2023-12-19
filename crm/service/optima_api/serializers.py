from django.core.exceptions import ObjectDoesNotExist

from crm.contractors.models import Contractor
from crm.core.optima import BaseOptimaSerializer
from crm.documents.models import DocumentType
from crm.service.models import Category, Device, DeviceType, ServiceOrder, Stage
from crm.users.models import User
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
            return User.objects.get(optima_id=self.obj[8])
        except ObjectDoesNotExist:
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
        }
