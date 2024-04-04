from crm.core.optima import OptimaObject


class ContractorObject(OptimaObject):
    table_name = "CDN.Kontrahenci"

    get_queryset = (
        "SELECT Knt.Knt_KntId, Knt.Knt_Kod, Knt.Knt_KodPocztowy, Knt.Knt_Nip, Knt.Knt_Telefon1, "
        "Knt.Knt_Kraj, Knt.Knt_Miasto, Knt.Knt_Ulica, Knt.Knt_NrDomu, Knt.Knt_NrLokalu, Knt.Knt_Poczta, "
        "Knt.Knt_Wojewodztwo, Knt.Knt_Nazwa1, Knt.Knt_Nazwa2, Knt.Knt_Nazwa3 "
        "FROM CDN.Kontrahenci as Knt"
    )
