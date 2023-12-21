from crm.core.optima import OptimaObject


class DocumentTypeObject(OptimaObject):
    get_queryset = (
        "SELECT DD.DDf_DDfID, DD.DDf_Klasa, DD.DDf_Symbol, DDf_Nazwa, DDf_Numeracja, DDf_Niekatywna "
        "FROM CDN.DokDefinicje as DD"
    )
