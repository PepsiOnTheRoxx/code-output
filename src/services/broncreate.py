from src.services.broncreate_exceptions import BronAlreadyExistsException, InvalidBronDataException

class BronRepository:
    def exists_bron(self, naam):
        # Placeholder for repository method
        raise NotImplementedError

    def save_bron(self, bron_data):
        # Placeholder for repository method
        raise NotImplementedError

class BronService:
    def __init__(self):
        self.repository = BronRepository()

    def create_bron(self, bron_data):
        naam = bron_data.get("naam")
        attr_15 = bron_data.get("attribute_15")
        attr_16 = bron_data.get("attribute_16")
        if not naam or not isinstance(naam, str) or naam.strip() == "":
            raise InvalidBronDataException("Naam is ongeldig of ontbreekt.")
        if attr_15 is None or attr_15 == "":
            raise InvalidBronDataException("attribute_15 is ongeldig of ontbreekt.")
        if attr_16 is None or attr_16 == "":
            raise InvalidBronDataException("attribute_16 is ongeldig of ontbreekt.")

        if self.repository.exists_bron(naam):
            raise BronAlreadyExistsException(f"Bron met naam '{naam}' bestaat al.")

        try:
            bron = self.repository.save_bron(bron_data)
        except Exception as e:
            raise
        return bron