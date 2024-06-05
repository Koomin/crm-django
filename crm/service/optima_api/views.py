from crm.core.optima import OptimaObject


class ServiceOptimaObject(OptimaObject):
    def get(self, *args):
        self.get_queryset = self.get_queryset.format(*args)
        return super().get()


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
        "SELECT SRS.SrU_SrUId, SRS.SrU_Kod, SRS.SrU_Nazwa, SRS.SrU_Opis, SRS.SrU_SrRId, Atrybuty.TwA_WartoscTxt "
        "FROM CDN.SrsUrzadzenia as SRS "
        "INNER JOIN CDN.TwrAtrybuty as Atrybuty ON SRS.SrU_SrUId = Atrybuty.TwA_SrUId "
        "WHERE Atrybuty.TwA_DeAId = 160"
    )


class AttributeDefinitionObject(OptimaObject):
    get_queryset = "SELECT DA.DeA_DeAId, DA.DeA_Kod, DA.DeA_Typ, DA.DeA_Format FROM CDN.DefAtrybuty as DA"


class AttributeDefinitionItemObject(OptimaObject):
    get_queryset = "SELECT DAE.DAE_DAEId, DAE.DAE_Wartosc, DAE.DAE_Lp, DAE.DAE_DeAId FROM CDN.DefAtrElem as DAE"


class AttributeObject(ServiceOptimaObject):
    table_name = "CDN.DokAtrybuty"
    id_field = "DAt_DAtId"
    get_queryset = (
        "SELECT DA.DAt_DAtId, DA.DAt_Kod, DA.DAt_DeAId, DA.DAt_WartoscTxt, DA.DAt_SrZId, DEF.DeA_Format "
        "FROM CDN.DokAtrybuty as DA "
        "INNER JOIN CDN.DefAtrybuty as DEF ON DA.DAt_DeAId=DEF.DeA_DeAId "
        "WHERE DA.DAt_SrZId = {0}"
    )


class ServiceOrderObject(ServiceOptimaObject):
    table_name = "CDN.SrsZlecenia"
    id_field = "SrZ_SrZId"
    get_queryset = (
        "SELECT SRS.SrZ_SrZId, SRS.SrZ_DDfId, SRS.SrZ_KatID, SRS.SrZ_NumerString, SRS.SrZ_NumerNr, "
        "SRS.SrZ_Bufor, SRS.SrZ_Stan, SRS.SrZ_PodmiotId, SRS.SrZ_OpeZalId, SRS.SrZ_DataDok, "
        "SRS.SrZ_DataPrzyjecia, SRS.SrZ_DataRealizacji, SRS.SrZ_DataZamkniecia, SRS.SrZ_MagId, "
        "SRS.SrZ_EtapId, SRS.SrZ_WartoscNetto, SRS.SrZ_WartoscBrutto, SRS.SrZ_Opis, SRS.SrZ_SrUId, "
        "SRS.SrZ_NumerPelny, SRS.SrZ_Email, SRS.SrZ_Telefon, SRS.SrZ_PodKraj, SRS.SrZ_PodMiasto, "
        "SRS.SrZ_PodNazwa1, SRS.SrZ_PodNazwa2, SRS.SrZ_PodNazwa3, SRS.SrZ_PodNrDomu, SRS.SrZ_PodNrLokalu, "
        "SRS.SrZ_PodPoczta, SRS.SrZ_PodUlica, SRS.SrZ_PodWojewodztwo, SRS.SrZ_PodmiotTyp, "
        "SRS.SrZ_PodKodPocztowy "
        "FROM CDN.SrsZlecenia as SRS WHERE SRS.SrZ_DDfId = {0} AND SRS.SrZ_DataDok >= '{1}'"
    )

    get_queryset_optima_id = (
        "SELECT SRS.SrZ_SrZId, SRS.SrZ_DDfId, SRS.SrZ_KatID, SRS.SrZ_NumerString, SRS.SrZ_NumerNr, "
        "SRS.SrZ_Bufor, SRS.SrZ_Stan, SRS.SrZ_PodmiotId, SRS.SrZ_OpeZalId, SRS.SrZ_DataDok, "
        "SRS.SrZ_DataPrzyjecia, SRS.SrZ_DataRealizacji, SRS.SrZ_DataZamkniecia, SRS.SrZ_MagId, "
        "SRS.SrZ_EtapId, SRS.SrZ_WartoscNetto, SRS.SrZ_WartoscBrutto, SRS.SrZ_Opis, SRS.SrZ_SrUId, "
        "SRS.SrZ_NumerPelny, SRS.SrZ_Email, SRS.SrZ_Telefon, SRS.SrZ_PodKraj, SRS.SrZ_PodMiasto, "
        "SRS.SrZ_PodNazwa1, SRS.SrZ_PodNazwa2, SRS.SrZ_PodNazwa3, SRS.SrZ_PodNrDomu, SRS.SrZ_PodNrLokalu, "
        "SRS.SrZ_PodPoczta, SRS.SrZ_PodUlica, SRS.SrZ_PodWojewodztwo, SRS.SrZ_PodmiotTyp, "
        "SRS.SrZ_PodKodPocztowy "
        "FROM CDN.SrsZlecenia as SRS WHERE SRS.SrZ_SrZId = {0}"
    )
    get_queryset_last_number = (
        "SELECT MAX(SRS.SrZ_NumerNr) "
        "FROM CDN.SrsZlecenia as SRS "
        "WHERE SRS.SrZ_NumerString = '{0}' AND SRS.SrZ_DDfId = {1} AND SRS.SrZ_NumerNr >= {2}"
    )

    get_queryset_id_by_number = (
        "SELECT SRS.SrZ_SrZId FROM CDN.SrsZlecenia as SRS WHERE SRS.SrZ_NumerNr={0} AND SRS.SrZ_NumerString='{1}'"
    )

    get_queryset_full_number = "SELECT SRS.SrZ_NumerPelny FROM CDN.SrsZlecenia as SRS WHERE SRS.SrZ_SrZId={0}"

    def get_by_optima_id(self, optima_id):
        self.get_queryset = self.get_queryset_optima_id.format(optima_id)
        return super().get()

    def get_last_number(self, number_scheme, document_id, number):
        self.get_queryset = self.get_queryset_last_number.format(number_scheme, document_id, number)
        return super().get_one()

    def get_id_by_number(self, number, number_scheme):
        self.get_queryset = self.get_queryset_id_by_number.format(number, number_scheme)
        return super().get_one()[0]

    def get_full_number(self, optima_id):
        self.get_queryset = self.get_queryset_full_number.format(optima_id)
        return super().get_one()[0]


class NoteObject(ServiceOptimaObject):
    table_name = "CDN.SrsNotatki"
    id_field = "SrN_SrNId"
    get_queryset = (
        "SELECT SRS.SrN_SrNId, SRS.SrN_Lp, SRS.SrN_SerwisantTyp, SRS.SrN_SerwisantId, SRS.SrN_DataDok, SRS.SrN_Tresc, "
        "SRS.SrN_SrZId "
        "FROM CDN.SrsNotatki as SRS WHERE SRS.SrN_SrZId = {0}"
    )


class ServicePartObject(ServiceOptimaObject):
    get_queryset = (
        "SELECT SC.SrC_SrCId, SC.SrC_Lp, SC.SrC_TwrId, SC.SrC_MmZwrot, SC.SrC_SerwisantId, SC.SrC_MagId, "
        "SC.SrC_Status, SC.SrC_Dokument, SC.SrC_Fakturowac, SC.SrC_CenaNetto, SC.SrC_CenaBrutto, SC.SrC_Rabat, "
        "SC.SrC_Ilosc, SC.SrC_IloscPobierana, SC.SrC_IloscWydanaDisp, SC.SrC_JM, SC.SrC_SrZId "
        "FROM CDN.SrsCzesci as SC WHERE SC.SrC_SrZId = {0}"
    )


class ServiceActivityObject(ServiceOptimaObject):
    table_name = "CDN.SrsCzynnosci"
    get_queryset = (
        "SELECT SRS.SrY_SrYId, SRS.SrY_SrZId, SRS.SrY_Lp, SRS.SrY_TwrId, SRS.SrY_SerwisantId, SRS.SrY_Zakonczona, "
        "SRS.SrY_Fakturowac, SRS.SrY_DataWykonania, SRS.SrY_TerminOd, SRS.SrY_TerminDo, SRS.SrY_Rabat, "
        "SRS.SrY_CenaNetto, SRS.SrY_CenaBrutto, SRS.SrY_Ilosc, SRS.SrY_WartoscNetto, "
        "SRS.SrY_WartoscBrutto, SRS.SrY_JM, SrY_Stawka "
        "FROM CDN.SrsCzynnosci as SRS WHERE SRS.SrY_SrZId = {0}"
    )
