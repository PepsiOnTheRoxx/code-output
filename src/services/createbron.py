from src.services.createbron_exceptions import BronAlreadyExistsException, InvalidBronDataException

class BronService:
    def __init__(self):
        self.bron_repository = None

    def create_bron(self, naam, beschrijving):
        if not isinstance(naam, str) or not naam.strip():
            raise InvalidBronDataException("Naam mag niet leeg zijn")
        if not isinstance(beschrijving, str) or not beschrijving.strip():
            raise InvalidBronDataException("Beschrijving mag niet leeg zijn")
        if self.bron_repository.exists(naam):
            raise BronAlreadyExistsException(f"Bron met naam '{naam}' bestaat al")
        return self.bron_repository.create(naam, beschrijving)