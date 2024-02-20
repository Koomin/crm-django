import pyodbc
from django.conf import settings

from crm.core.exceptions import IsValidException


class BaseOptimaSerializer:
    required_fields = []
    model = None

    def __init__(self, obj):
        self._data = None
        self._valid = False
        self.obj = obj
        if isinstance(obj, self.model):
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
                return self._data
            else:
                raise IsValidException("is_valid() method wasn't called")
        return self._data


class OptimaConnection:
    def __init__(self, database=None):
        try:
            self.cnxn = pyodbc.connect(
                "Driver={ODBC Driver 17 for SQL Server};"
                f"Server={settings.OPTIMA_DB['SERVER']};"
                f"Database={settings.OPTIMA_DB['DATABASE'] if not database else database};"
                f"uid={settings.OPTIMA_DB['UID']};"
                f"pwd={settings.OPTIMA_DB['PASSWORD']}",
                autocommit=False,
            )
        except pyodbc.OperationalError:
            self.cnxn = None
            self.cursor = None
        else:
            self.cursor = self.cnxn.cursor()


class OptimaObject:
    get_queryset = None
    post_queryset = None
    fields = None
    table_name = None

    def __init__(self, database=None):
        self.connection = OptimaConnection(database).cursor

    def _prepare_insert_queryset(self, fields):
        return f"INSERT INTO {self.table_name} " f"({fields}) VALUES " f"({','.join('?' * len(fields))})"

    def get(self):
        return self.connection.execute(self.get_queryset).fetchall()

    def _get_optima_id(self):
        return self.connection.execute("SELECT @@Identity").fetchone()[0]

    def post(self, obj):
        fields = ",".join(field for field in obj.keys())
        insert_queryset = self._prepare_insert_queryset(fields)
        self.connection.execute(insert_queryset, obj.values())
        return self._get_optima_id()
