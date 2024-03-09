import pyodbc
from django.conf import settings

from crm.core.exceptions import IsValidException
from crm.crm_config.models import GeneralSettings


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
            self._valid = True
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
    def _default_db_values(self) -> dict:
        return {}

    @property
    def data(self):
        if not self._deserialization:
            if self._data and self._valid:
                if self._default_db_values:
                    return {**self._data, **self._default_db_values}
                else:
                    return self._data
            else:
                raise IsValidException("is_valid() method wasn't called")
        elif self._valid and self._deserialization:
            return self._data
        return None


class OptimaConnection:
    def __init__(self, database=None):
        general_settings = GeneralSettings.objects.all().first()
        if general_settings and general_settings.optima_general_database:
            general_db = general_settings.optima_general_database
        else:
            general_db = settings.OPTIMA_DB["DATABASE"]
        try:
            self.cnxn = pyodbc.connect(
                "Driver={ODBC Driver 17 for SQL Server};"
                f"Server={settings.OPTIMA_DB['SERVER']};"
                f"Database={general_db if not database else database};"
                f"uid={settings.OPTIMA_DB['UID']};"
                f"pwd={settings.OPTIMA_DB['PASSWORD']}",
                autocommit=True,
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

    def _prepare_insert_queryset(self, fields, values):
        return f"INSERT INTO {self.table_name} ({fields}) VALUES ({values})"

    def get(self):
        return self.connection.execute(self.get_queryset).fetchall()

    def _get_optima_id(self):
        return self.connection.execute("SELECT @@Identity").fetchone()[0]

    def post(self, obj):
        fields = ",".join(field for field in obj.keys())
        values = ",".join("?" * len(obj.keys()))
        insert_queryset = self._prepare_insert_queryset(fields, values)
        self.connection.execute(insert_queryset, tuple(obj.values()))
        return self._get_optima_id()
