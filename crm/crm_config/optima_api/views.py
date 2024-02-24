from crm.core.optima import OptimaObject


class StateObject(OptimaObject):
    get_queryset = (
        "SELECT TRT.Trt_TrtID, TRT.Trt_Nazwa, TRT.Trt_Powiat, TRT.Trt_Gmina "
        "FROM CDN.Teryt as TRT WHERE TRT.Trt_Powiat = 0 AND TRT.Trt_Gmina = 0"
    )

    def __init__(self):
        super().__init__(database="CDN_KNF_Konfiguracja")


class CountryObject(OptimaObject):
    get_queryset = "SELECT K.Kra_KraID, K.Kra_Nazwa, K.Kra_Kod FROM CDN.Kraje as K"

    def __init__(self):
        super().__init__(database="CDN_KNF_Konfiguracja")
