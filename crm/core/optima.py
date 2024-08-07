import datetime

import pyodbc
from django.apps import apps
from django.conf import settings

from crm.core.exceptions import IsValidException
from crm.crm_config.models import GeneralSettings, Log


class BaseOptimaSerializer:
    required_fields = []
    fields_mapping = {}
    _fields_updated = []
    model = None
    default_datetime = datetime.datetime(year=1899, month=12, day=30, hour=0, minute=0, second=0, microsecond=0)

    def __init__(self, obj, fields_updated=None):
        self._data = None
        self._valid = False
        self._errors = []
        self.obj = obj
        if isinstance(obj, self.model):
            self._fields_updated = fields_updated
            self.required_fields = self._override_required_fields()
            self._deserialization = False
        else:
            self._valid = True
            self._deserialization = True
            self._data = self._deserialize()

    def _override_required_fields(self):
        new_required_fields = []
        if self._fields_updated:
            for field in self._fields_updated:
                new_required_fields.extend(self.fields_mapping[field])
            return new_required_fields
        return self.required_fields

    @property
    def errors(self):
        return self._errors if not self._valid else 0

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
                        self._errors.append(f'Field "{field}" is required.')
                        self._data = None
                        return self._valid
                except KeyError:
                    self._errors.append(f'Field "{field}" is required.')
                    self._data = None
                    return self._valid
            self._valid = True
        else:
            self._valid = True
        return self._valid

    def _get_updated_serializer(self):
        _updated_serializer = {}
        for updated_field in self._fields_updated:
            for field in self.fields_mapping[updated_field]:
                _updated_serializer[field] = self._data[field]
        return _updated_serializer

    @property
    def _default_db_values(self) -> dict:
        return {}

    @property
    def data(self):
        if not self._deserialization:
            if self._data and self._valid:
                if self._default_db_values and not self._fields_updated:
                    return {**self._data, **self._default_db_values}
                elif self._fields_updated:
                    return self._get_updated_serializer()
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
            self.connection_string = (
                "Driver={ODBC Driver 17 for SQL Server};"
                f"Server={settings.OPTIMA_DB['SERVER']};"
                f"Database={general_db if not database else database};"
                f"uid={settings.OPTIMA_DB['UID']};"
                f"pwd={settings.OPTIMA_DB['PASSWORD']}"
            )
            self.cnxn = pyodbc.connect(
                self.connection_string,
                autocommit=False,
            )
        except Exception as e:
            self.cnxn = None
            self.cursor = None
            Log.objects.create(
                exception_traceback=e,
                method_name="__init__",
                model_name=self.__class__.__name__,
                object_serialized="",
            )
        else:
            self.cursor = self.cnxn.cursor()


class OptimaObject:
    get_queryset = None
    post_queryset = None
    fields = None
    table_name = None
    id_field = None

    def __init__(self, database=None):
        self._synchronize = self._get_synchronize()
        if self._synchronize:
            try:
                self.connection_ = OptimaConnection(database)
                self.connection = self.connection_.cursor
                if not self.connection:
                    raise Exception("Connection error, check env variables.")
            except Exception as e:
                self._connection_error = e
                self.connection = None
                Log.objects.create(
                    exception_traceback=e,
                    method_name="__init__",
                    model_name=self.__class__.__name__,
                    object_serialized="",
                )
        else:
            self._connection_error = "Synchronization is disabled."
            self.connection = None

    def _get_synchronize(self):
        general_settings_model = apps.get_model("crm_config", "GeneralSettings")
        try:
            general_settings = general_settings_model.objects.first()
        except general_settings_model.DoesNotExist:
            return False
        return general_settings.optima_synchronization

    def _prepare_insert_queryset(self, fields, values):
        return f"INSERT INTO {self.table_name} ({fields}) VALUES ({values})"

    @staticmethod
    def _prepare_fields_string(fields):
        return ",".join([f"{field}=?" for field in fields])

    def _prepare_update_queryset(self, fields):
        return f"UPDATE {self.table_name} SET {self._prepare_fields_string(fields)} WHERE {self.id_field}=?"

    @staticmethod
    def _prepare_update_values(values, optima_id):
        values_list = list(values)
        values_list.append(optima_id)
        return tuple(values_list)

    def _get_optima_id(self):
        try:
            return self.connection.execute("SELECT @@Identity").fetchone()[0]
        except Exception as e:
            Log.objects.create(
                exception_traceback=e,
                method_name="_get_optima_id",
                model_name=self.__class__.__name__,
                object_serialized="",
            )
            return

    def get(self):
        try:
            return self.connection.execute(self.get_queryset).fetchall()
        except Exception as e:
            Log.objects.create(
                exception_traceback=e,
                method_name="get",
                model_name=self.__class__.__name__,
                object_serialized="",
            )
            return

    def get_one(self):
        try:
            return self.connection.execute(self.get_queryset).fetchone()
        except Exception as e:
            Log.objects.create(
                exception_traceback=e,
                method_name="get",
                model_name=self.__class__.__name__,
                object_serialized="",
            )
            return

    def post(self, obj) -> (bool, str):
        fields = ",".join(field for field in obj.keys())
        values = ",".join("?" * len(obj.keys()))
        insert_queryset = self._prepare_insert_queryset(fields, values)
        if self._synchronize and self.connection:
            try:
                self.connection.execute(insert_queryset, tuple(obj.values()))
                optima_id = self._get_optima_id()
            except Exception as e:
                self.connection.rollback()
                return False, e
            else:
                self.connection.commit()
                Log.objects.create(
                    status=Log.Status.INFO,
                    method_name="post",
                    model_name=self.__class__.__name__,
                    object_serialized=f"{insert_queryset}, {' ,'.join(str(_) for _ in obj.values())}",
                )
            return True, optima_id
        elif self._synchronize and not self.connection:
            return False, self._connection_error
        else:
            return False, "Synchronization is disabled"

    def put(self, obj, optima_id):
        update_queryset = self._prepare_update_queryset(obj.keys())
        values = self._prepare_update_values(obj.values(), optima_id)
        if self._synchronize and self.connection:
            try:
                self.connection.execute(update_queryset, values)
            except Exception as e:
                self.connection.rollback()
                return False, e
            else:
                self.connection.commit()
                Log.objects.create(
                    status=Log.Status.INFO,
                    method_name="put",
                    model_name=self.__class__.__name__,
                    object_serialized=f"{update_queryset}, {' ,'.join(str(_) for _ in values)}",
                )
            return True, "Updated"
        elif self._synchronize and not self.connection:
            return False, self._connection_error
        else:
            return False, "Synchronization is disabled"
