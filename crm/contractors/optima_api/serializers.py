import datetime

from crm.contractors.models import Contractor
from crm.core.optima import BaseOptimaSerializer


class ContractorSerializer(BaseOptimaSerializer):
    model = Contractor

    def _get_name(self):
        return (self.obj[12] + " " + self.obj[13] + " " + self.obj[14]).strip()

    def _get_home_number(self):
        try:
            _home_number = int(self.obj[9])
        except ValueError:
            return None
        else:
            return _home_number

    def _deserialize(self) -> dict:
        return {
            "optima_id": self.obj[0],
            "code": self.obj[1],
            "postal_code": self.obj[2],
            "tax_number": self.obj[3],
            "phone_number": self.obj[4],
            "country": self.obj[5],
            "city": self.obj[6],
            "street": self.obj[7],
            "street_number": self.obj[8],
            "home_number": self._get_home_number(),
            "post": self.obj[10],
            "state": self.obj[11],
            "name": self._get_name(),
            "name1": self.obj[12],
            "name2": self.obj[13],
            "name3": self.obj[14],
            "regon": self.obj[15],
            "confirmed": True,
            "exported": True,
        }

    def _serialize(self) -> dict:
        return {
            "Knt_KodPocztowy": self.obj.postal_code,
            "Knt_Nip": self.obj.tax_number,
            "Knt_NipE": self.obj.tax_number,
            "Knt_Telefon1": self.obj.phone_number,
            "Knt_Kraj": self.obj.country,
            "Knt_Miasto": self.obj.city,
            "Knt_Ulica": self.obj.street,
            "Knt_NrDomu": self.obj.street_number,
            "Knt_NrLokalu": self.obj.home_number,
            "Knt_Poczta": self.obj.post,
            "Knt_Wojewodztwo": self.obj.state,
            "Knt_Nazwa1": self.obj.name1,
            "Knt_Nazwa2": self.obj.name2 if self.obj.name2 else " ",
            "Knt_Nazwa3": self.obj.name3 if self.obj.name3 else " ",
            "Knt_Regon": self.obj.regon,
            # TODO Check how to autocreate Knt_Kod
            # "Knt_Kod": self.obj.tax_number,
        }

    @property
    def _default_db_values(self) -> dict:
        return {
            "Knt_NipKraj": "",
            "Knt_PodmiotTyp": 1,
            "Knt_GLN": "",
            "Knt_EAN": "",
            "Knt_Telefon2": "",
            "Knt_Fax": "",
            "Knt_URL": "",
            "Knt_IBAN": 1,
            "Knt_OsPlec": 1,
            "Knt_OsKodPocztowy": "",
            "Knt_OsTelefon": "",
            "Knt_OsGSM": "",
            "Knt_Informacje": 0,
            "Knt_Upust": 0.00,
            "Knt_LimitFlag": 0,
            "Knt_LimitKredytu": 0.00,
            "Knt_LimitPrzeterKredytFlag": 0.00,
            "Knt_LimitPrzeterKredytWartosc": 0.00,
            "Knt_Ceny": 0,
            "Knt_MaxZwloka": 0,
            "Knt_TerminPlat": 7,
            "Knt_Termin": 7,
            "Knt_BlokadaDok": 0,
            "Knt_LimitKredytuWal": "",
            "Knt_LimitKredytuWykorzystany": 0,
            "Knt_NieRozliczac": 0,
            "Knt_PodatekVat": 1,
            "Knt_Finalny": 0,
            "Knt_Export": 0,
            "Knt_Rodzaj": 0,
            "Knt_Rodzaj_Dostawca": 1,
            "Knt_Rodzaj_Odbiorca": 0,
            "Knt_Rodzaj_Konkurencja": 0,
            "Knt_Rodzaj_Partner": 0,
            "Knt_Rodzaj_Potencjalny": 0,
            "Knt_Medialny": 0,
            "Knt_MalyPod": 0,
            "Knt_Rolnik": 0,
            "Knt_Nieaktywny": 0,
            "Knt_Chroniony": 0,
            "Knt_OpiekunKsiegDomyslny": 1,
            "Knt_OpiekunPiKDomyslny": 0,
            "Knt_TerminZwrotuKaucji": 60,
            "Knt_NaliczajPlatnosc": 0,
            "Knt_ZakazDokumentowHaMag": 0,
            "Knt_ZgodaNaEFaktury": 0,
            "Knt_TS_Zal": datetime.datetime.now(),
            "Knt_TS_Mod": datetime.datetime.now(),
            "Knt_Adres2": "",
            "Knt_Gmina": "",
            "Knt_Email": "-",
            "Knt_Grupa": "DOSTAWCA",
            "Knt_KodTransakcji": "",
            "Knt_KontoDost": "",
            "Knt_KontoOdb": "",
            "Knt_KrajISO": "",
            "Knt_Opis": "",
            "Knt_OsAdres2": "",
            "Knt_OsEmail": "",
            "Knt_OsGmina": "",
            "Knt_OsKraj": "",
            "Knt_OsMiasto": "",
            "Knt_OsNazwisko": "",
            "Knt_OsNrDomu": "",
            "Knt_OsNrLokalu": "",
            "Knt_OsPoczta": "",
            "Knt_OsPowiat": "",
            "Knt_OsTytul": "",
            "Knt_OsUlica": "",
            "Knt_OsWojewodztwo": "",
            "Knt_Pesel": "",
            "Knt_Powiat": "",
            "Knt_RachunekNr": "",
            # TODO Check Knt_Zezwolenie
            "Knt_Zezwolenie": "wpis",
            "Knt_FCzynnosci": "",
            "Knt_FCzesci": "",
            "Knt_ZwolnionyZAkcyzy": 0,
            "Knt_PowiazanyUoV": 0,
            "Knt_NieNaliczajOdsetek": 0,
            "Knt_ESklep": 0,
            "Knt_WindykacjaEMail": "",
            "Knt_TelefonSms": "",
            "Knt_WindykacjaTelefonSms": "",
            "Knt_MetodaKasowa": 0,
            "Knt_FinalnyWegiel": 0,
            "Knt_Komornik": 0,
            "Knt_Waluta": "",
            "Knt_Algorytm": 0,
            "Knt_NieUwzglVATZD": 0,
            "Knt_OpeModKod": "",
            "Knt_OpeModNazwisko": "",
            "Knt_OpeZalKod": "",
            "Knt_OpeZalNazwisko": "",
            "Knt_OpiekunDomyslny": 1,
            "Knt_LpAnonimizacji": 0,
            "Knt_SplitPay": 0,
            "Knt_Domena": "",
            "Knt_DokumentTozsamosci": "",
            "Knt_UmowaWegiel": 0,
            "Knt_IdSisc": "",
            "Knt_eSklepZrodlo": "",
            "Knt_AwfZgoda": 0,
            "Knt_AwfMonit": 0,
            "Knt_NieNaliczajOplataCukrowa": 0,
            "Knt_NieUwzglwedniajWEwidencjiWegiel": 0,
            "Knt_NieWysylajDokumentuDoKSeF": 0,
        }


class ContractorAttributeSerializer(BaseOptimaSerializer):
    def __init__(self, obj, code):
        self._data = None
        self._valid = False
        self._errors = []
        self.obj = obj
        self.code = code
        self._deserialization = False

    def _serialize(self) -> dict:
        return {
            "KnA_PodmiotId": self.obj.optima_id,
            "KnA_PodmiotTyp": 1,
            "KnA_DeAId": self.code,
            "KnA_WartoscTxt": "DF",
        }
