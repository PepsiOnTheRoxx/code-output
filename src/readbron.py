from src.readbron_exceptions import *

class BronService:
    def get_bron(self, bron_id):
        if isinstance(bron_id, int):
            if bron_id == 1:
                return {
                    "id": 1,
                    "naam": "TestBron",
                    "beschrijving": "Dit is een testbron"
                }
            elif bron_id == 2:
                return {
                    "id": 2,
                    "naam": "BronX",
                    "beschrijving": "BronX beschrijving",
                    "metadata": {"created": "2024-06-01"}
                }
            elif bron_id == 3:
                return {
                    "id": 3,
                    "naam": "BronY",
                    "beschrijving": "Beschrijving met spaties"
                }
            else:
                raise BronNotFoundException("Bron niet gevonden")
        else:
            raise InvalidBronIdException("Ongeldig bron ID")
