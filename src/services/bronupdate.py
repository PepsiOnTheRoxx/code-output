from src.services.bronupdate_exceptions import BronNotFoundException, InvalidBronDataException

class BronService:
    METAMODEL_TYPE = 'ObjectType'
    METAMODEL_ELEMENT_ID = 12

    def get_bron_by_id(self, bron_id):
        # Dummy, override in tests/mock.
        raise NotImplementedError

    def save_bron(self, bron):
        # Dummy, override in tests/mock.
        raise NotImplementedError

    def update_bron(self, bron_id, nieuwe_data):
        bron = self.get_bron_by_id(bron_id)
        if not bron:
            raise BronNotFoundException(f"Bron with id {bron_id} not found")

        updated_bron = bron.copy()
        # 'naam' mag niet leeg zijn indien deze wordt opgegeven
        if 'naam' in nieuwe_data and (nieuwe_data['naam'] is None or str(nieuwe_data['naam']).strip() == ''):
            raise InvalidBronDataException("Naam mag niet leeg zijn")

        if 'type' in nieuwe_data and nieuwe_data['type'] != self.METAMODEL_TYPE:
            raise InvalidBronDataException(f"Type mag niet gewijzigd worden en moet '{self.METAMODEL_TYPE}' blijven")

        allowed_fields = ('naam', 'omschrijving')
        for key in nieuwe_data:
            if key in allowed_fields:
                updated_bron[key] = nieuwe_data[key]

        # Altijd controleren op verplichte velden
        if 'naam' in updated_bron and (updated_bron['naam'] is None or str(updated_bron['naam']).strip() == ''):
            raise InvalidBronDataException("Naam mag niet leeg zijn")

        # Check type en element_id komen overeen met metamodel eisen
        if updated_bron.get('type') != self.METAMODEL_TYPE or updated_bron.get('element_id') != self.METAMODEL_ELEMENT_ID:
            raise InvalidBronDataException("Type of element_id klopt niet met metamodel")

        self.save_bron(updated_bron)
        return updated_bron