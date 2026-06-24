from src.createvernietigingstaak_exceptions import *

class Vernietigingstaak:
    def __init__(self, aantekeningen, datum, status):
        self.aantekeningen = aantekeningen
        self.datum = datum
        self.status = status

class VernietigingstaakService:
    ALLOWED_STATUS = {"InBehandeling", "Afgerond"}

    def create_vernietigingstaak(self, aantekeningen, datum, status):
        if aantekeningen is None or not isinstance(aantekeningen, str) or aantekeningen.strip() == "":
            raise MissingAantekeningenException()
        if datum is None:
            raise MissingDatumException()
        if status not in self.ALLOWED_STATUS:
            raise InvalidStatusException()
        return Vernietigingstaak(aantekeningen, datum, status)