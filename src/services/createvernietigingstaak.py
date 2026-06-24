from src.services.createvernietigingstaak_exceptions import InvalidStatusException, MissingAttributeException

class Vernietigingstaak:
    def __init__(self, aantekeningen, datum, status):
        self.aantekeningen = aantekeningen
        self.datum = datum
        self.status = status

class VernietigingstaakRepository:
    def create(self, aantekeningen, datum, status):
        return Vernietigingstaak(aantekeningen, datum, status)

class VernietigingstaakService:
    VALID_STATUSES = {"GEPLAND", "IN_UITVOERING", "VOLTOOID"}

    def __init__(self):
        self.repository = VernietigingstaakRepository()

    def create_vernietigingstaak(self, *, aantekeningen=None, datum=None, status=None):
        if aantekeningen is None:
            raise MissingAttributeException("Attribute 'aantekeningen' is required")
        if datum is None:
            raise MissingAttributeException("Attribute 'datum' is required")
        if status is None:
            raise MissingAttributeException("Attribute 'status' is required")
        if status not in self.VALID_STATUSES:
            raise InvalidStatusException(f"Invalid status: {status}")
        return self.repository.create(aantekeningen, datum, status)