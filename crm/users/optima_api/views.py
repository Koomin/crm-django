from crm.core.optima import OptimaObject


class UserObject(OptimaObject):
    get_queryset = "SELECT OPE.Ope_OpeID, OPE.Ope_Nazwisko, OPE.Ope_Kod FROM CDN.Operatorzy as OPE"

    def __init__(self):
        super().__init__(database="CDN_KNF_Konfiguracja")
