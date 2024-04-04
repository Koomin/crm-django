from crm.core.optima import OptimaObject


class WarehouseObject(OptimaObject):
    get_queryset = (
        "SELECT Mag.Mag_MagId, Mag.Mag_Typ, Mag.Mag_Symbol, Mag.Mag_NieAktywny, Mag.Mag_Nazwa, Mag.Mag_Opis,"
        " Mag.Mag_Rejestr "
        "FROM CDN.Magazyny as Mag"
    )
