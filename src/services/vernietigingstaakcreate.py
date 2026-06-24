from datetime import date
from src.services.vernietigingstaakcreate_exceptions import (
    InvalidDatumException,
    InvalidStatusException,
    MissingAantekeningenException,
)


class Vernietigingstaak:
    def __init__(self, aantekeningen, datum, status):
        self.aantekeningen = aantekeningen
        self.datum = datum
        self.status = status


class VernietigingstaakService:
    ALLOWED_STATUS_VALUES = {"AANGEVRAAGD", "IN_BEHANDELING"}

    def create(self, aantekeningen, datum, status):
        if not aantekeningen or not isinstance(aantekeningen, str) or aantekeningen.strip() == "":
            raise MissingAantekeningenException()
        if datum > date.today():
            raise InvalidDatumException()
        if status not in self.ALLOWED_STATUS_VALUES:
            raise InvalidStatusException()
        return Vernietigingstaak(aantekeningen=aantekeningen, datum=datum, status=status)
