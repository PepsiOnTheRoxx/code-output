from src.services.bronread_exceptions import BronNotFoundException, BronReadException

class BronService:
    def __init__(self):
        # Simuleer opslag met wat dummy data
        self._bronnen = {
            1: {"id": 1, "naam": "Bron A", "type": "Type X"},
            2: {"id": 2, "naam": "Bron B", "type": None},
            3: {"id": 3, "naam": "Bron C", "type": "Type Y"},
        }

    def _lees_bron(self, bron_id):
        # interne, niet zichtbaar voor monkeypatch
        if bron_id is None or not isinstance(bron_id, int):
            raise BronReadException(f"Bron ID '{bron_id}' is ongeldig")
        if bron_id not in self._bronnen:
            raise BronNotFoundException(f"Bron met ID {bron_id} niet gevonden")
        bron = self._bronnen[bron_id]
        return bron

    def lees_bron(self, bron_id):
        try:
            return self._lees_bron(bron_id)
        except BronNotFoundException:
            raise
        except BronReadException:
            raise
        except Exception as e:
            raise BronReadException(str(e)) from e
