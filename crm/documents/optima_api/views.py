from crm.core.optima import OptimaObject


class DocumentTypeObject(OptimaObject):
    get_queryset = (
        "SELECT DD.DDf_DDfID, DD.DDf_Klasa, DD.DDf_Symbol, DD.DDf_Nazwa, DD.DDf_Numeracja, DD.DDf_Niekatywna "
        "FROM CDN.DokDefinicje as DD"
    )
