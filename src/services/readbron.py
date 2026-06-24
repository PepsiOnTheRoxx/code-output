from src.services.readbron_exceptions import (
    ReadBronDataNotFoundException,
    ReadBronInvalidElementIDException
)

class BronNotFoundException(ReadBronDataNotFoundException):
    pass

class InvalidBronIDException(ReadBronInvalidElementIDException):
    pass

class BronService:
    _bron_data = {
        1: {"ElementType": "ObjectType", "ElementID": 12},
    }

    def read_bron(self, bron_id):
        if bron_id is None or not isinstance(bron_id, int):
            raise InvalidBronIDException(f"Invalid bron_id: {bron_id}")
        bron = self._bron_data.get(bron_id)
        if not bron:
            raise BronNotFoundException(f"Bron with id {bron_id} not found")
        return dict(bron)