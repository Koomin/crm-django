import json

from crm.core.exceptions import IsValidException


class BaseOptimaSerializer:
    required_fields = []
    model = None

    def __init__(self, obj):
        self._data = None
        self._valid = False
        if isinstance(obj, self.model):
            self.obj = obj
            self._deserialization = False
        else:
            self._deserialization = True
            self._data = self._deserialize()

    def _serialize(self) -> dict:
        pass

    def _deserialize(self) -> dict:
        pass

    def is_valid(self, safe=True) -> bool:
        self._data = self._serialize()
        if safe:
            if self.required_fields != "__all__":
                _fields_to_check = self.required_fields
            else:
                _fields_to_check = self._data.keys()
            for field in _fields_to_check:
                try:
                    if self._data[field] is not None:
                        pass
                    else:
                        self._data = None
                except KeyError:
                    self._data = None
                    return self._valid
            self._valid = True
        else:
            self._valid = True
        return self._valid

    @property
    def data(self):
        if not self._deserialization:
            if self._data and self._valid:
                return json.dumps(self._data)
            else:
                raise IsValidException("is_valid() method wasn't called")
        return self._data


class OptimaConnection:
    pass


class OptimaObject:
    query = None

    def __init__(self):
        self.connection = OptimaConnection()

    def get(self):
        pass

    def post(self):
        pass
