from crm.core.optima import OptimaObject


class ProductGroupObject(OptimaObject):
    get_queryset = "SELECT Towary.TwG_TwGID, Towary.TwG_Kod, Towary.TwG_Nazwa FROM CDN.TwrGrupy as Towary"


class ProductObject(OptimaObject):
    get_queryset = (
        "SELECT Towary.Twr_TwrId, Towary.Twr_Kod, Towary.Twr_Nazwa, Towary.Twr_JM, "
        "Towary.Twr_Typ, Towary.Twr_TwCNumer FROM CDN.Towary as Towary"
    )
