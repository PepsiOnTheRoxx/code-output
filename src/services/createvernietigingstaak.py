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
        # Only treat status as missing if it is not provided AT ALL, not if it's None due to the test wants to allow InvalidStatusException on None.
        if status is None or status == "":
            raise InvalidStatusException(f"Invalid status: {status}")
        if status not in self.VALID_STATUSES:
            raise InvalidStatusException(f"Invalid status: {status}")
        return self.repository.create(aantekeningen, datum, status)
