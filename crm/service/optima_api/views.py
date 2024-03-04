from crm.core.optima import OptimaObject


class CategoryObject(OptimaObject):
    get_queryset = (
        "SELECT Kat.Kat_KatID, Kat.Kat_KodOgolny, Kat.Kat_KodSzczegol, Kat.Kat_Opis FROM CDN.Kategorie as Kat"
    )


class StageObject(OptimaObject):
    get_queryset = "SELECT DE.DEt_DEtId, DE.DEt_Typ, DE.DEt_Kod, DE.DEt_Opis FROM CDN.DefEtapy as DE"


class DeviceTypeObject(OptimaObject):
    get_queryset = "SELECT SRS.SrR_SrRId, SRS.SrR_Kod, SRS.SrR_Nieaktywny, SRS.SrR_Nazwa FROM CDN.SrsRodzajeU as SRS"


class DeviceObject(OptimaObject):
    get_queryset = (
        "SELECT SRS.SrU_SrUId, SRS.SrU_Kod, SRS.SrU_Nazwa, SRS.SrU_Opis, SRS.SrU_SrRId"
        " FROM CDN.SrsUrzadzenia as SRS"
    )


class AttributeDefinitionObject(OptimaObject):
    get_queryset = "SELECT DA.DeA_DeAId, DA.DeA_Kod, DA.DeA_Typ, DA.DeA_Format FROM CDN.DefAtrybuty as DA"


class AttributeDefinitionItemObject(OptimaObject):
    get_queryset = "SELECT DAE.DAE_DAEId, DAE.DAE_Wartosc, DAE.DAE_Lp, DAE.DAE_DeAId FROM CDN.DefAtrElem as DAE"


class AttributeObject(OptimaObject):
    get_queryset = (
        "SELECT DA.DAt_DAtId, DA.DAt_Kod, DA.DAt_DeAId, DA.DAt_WartoscTxt, DA.DAt_SrZId "
        "FROM CDN.DokAtrybuty as DA WHERE DA.DAt_SrZId = {0}"
    )

    def get(self, order_id):
        self.get_queryset = self.get_queryset.format(order_id)
        return super().get()


class ServiceOrderObject(OptimaObject):
    get_queryset = (
        "SELECT SRS.SrZ_SrZId, SRS.SrZ_DDfId, SRS.SrZ_KatID, SRS.SrZ_NumerString, SRS.SrZ_NumerNr, "
        "SRS.SrZ_Bufor, SRS.SrZ_Stan, SRS.SrZ_PodmiotId, SRS.SrZ_OpeZalId, SRS.SrZ_DataDok, "
        "SRS.SrZ_DataPrzyjecia, SRS.SrZ_DataRealizacji, SRS.SrZ_DataZamkniecia, SRS.SrZ_MagId, "
        "SRS.SrZ_EtapId, SRS.SrZ_WartoscNetto, SRS.SrZ_WartoscBrutto, SRS.SrZ_Opis, SRS.SrZ_SrUId, "
        "SRS.SrZ_NumerPelny, SRS.SrZ_Email, SRS.SrZ_Telefon, SRS.SrZ_PodKraj, SRS.SrZ_PodMiasto, "
        "SRS.SrZ_PodNazwa1, SRS.SrZ_PodNazwa2, SRS.SrZ_PodNazwa3, SRS.SrZ_PodNrDomu, SRS.SrZ_PodNrLokalu, "
        "SRS.SrZ_PodPoczta, SRS.SrZ_PodUlica, SRS.SrZ_PodWojewodztwo, SRS.SrZ_PodmiotTyp, "
        "SRS.SrZ_PodKodPocztowy "
        "FROM CDN.SrsZlecenia as SRS"
    )


class NoteObject(OptimaObject):
    get_queryset = (
        "SELECT SRS.SrN_SrNId, SRS.SrN_Lp, SRS.SrN_SerwisantTyp, SRS.SrN_SerwisantId, SRS.SrN_DataDok, SRS.SrN_Tresc, "
        "SRS.SrN_SrZId "
        "FROM CDN.SrsNotatki as SRS"
    )


class ServicePartObject(OptimaObject):
    get_queryset = (
        "SELECT SC.SrC_SrCId, SC.SrC_Lp, SC.SrC_TwrId, SC.SrC_MmZwrot, SC.SrC_SerwisantId, SC.SrC_MagId, "
        "SC.SrC_Status, SC.SrC_Dokument, SC.SrC_Fakturowac, SC.SrC_CenaNetto, SC.SrC_CenaBrutto, SC.SrC_Rabat, "
        "SC.SrC_Ilosc, SC.SrC_IloscPobierana, SC.SrC_IloscWydanaDisp, SC.SrC_JM, SC.SrC_SrZId "
        "FROM CDN.SrsCzesci as SC WHERE SC.SrC_SrZId = {0}"
    )

    def get(self, order_id):
        self.get_queryset = self.get_queryset.format(order_id)
        return super().get()
