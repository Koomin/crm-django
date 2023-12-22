from crm.core.optima import OptimaObject


class CategoryObject(OptimaObject):
    get_queryset = (
        "SELECT Kat.Kat_KatID, Kat.Kat_KodOgolny, Kat.Kat_KodSzczegol, Kat.Kat_Opis " "FROM CDN.Kategorie as Kat"
    )


class StageObject(OptimaObject):
    get_queryset = "SELECT DE.DEt_DEtId, DE.DEt_Typ, DE.DEt_Kod, DE.DEt_Opis " "FROM CDN.DefEtapy as DE"


class DeviceTypeObject(OptimaObject):
    get_queryset = (
        "SELECT SRS.SrR_SrRId, SRS.SrR_Kod, SRS.SrR_Nieaktywny, SRS.SrR_Nazwa " "FROM CDN.SrsRodzajeU as SRS"
    )


class DeviceObject(OptimaObject):
    get_queryset = (
        "SELECT SRS.SrU_SrUId, SRS.SrU_Kod, SRS.SrU_Nazwa, SRS.SrU_Opis, SRS.SrU_SrRId"
        " FROM CDN.SrsUrzadzenia as SRS"
    )


class ServiceOrderObject(OptimaObject):
    get_queryset = (
        "SELECT SRS.SrZ_SrZId, SRS.SrZ_DDfId, SRS.SrZ_KatID, SRS.SrZ_NumerString, SRS,SrZ_NumerNr, "
        "SRS.SrZ_Bufor, SRS.SrZ_Stan, SRS.SrZ_PodmiotId, SRS.SrZ_OpeZalId, SRS.SrZ_DataDok, "
        "SRS.SrZ_DataPrzyjecia, SRS.SrZ_DataRealizacji, SRS.SrZ_DataZamkniecia, SRS.SrZ_MagId, "
        "SRS.SrZ_EtapId, SRS.SrZ_WartoscNetto, SRS.SrZ_WartoscBrutto, SRS.SrZ_Opis, SRS.SrZ_SrUId "
        "FROM CDN.SrsZlecenia as SRS"
    )