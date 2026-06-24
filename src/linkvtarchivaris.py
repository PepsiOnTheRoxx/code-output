from src.linkvtarchivaris_exceptions import *

class VernietigingstaakRelatiesService:
    def __init__(self):
        self._gebruikers = {
            100: {'id': 100, 'rechten': True},
            110: {'id': 110, 'rechten': True},
            120: {'id': 120, 'rechten': True},  # Default; kan aangepast worden met set_rechten
        }
        self._vernietigingstaken = {
            200: {'id': 200},
            220: {'id': 220},
            230: {'id': 230},
        }
        self._gekoppelde_archivarissen = set()  # Set van (gebruiker_id, taak_id)
        self._rechten_overrides = {}  # gebruiker_id -> bool

    def set_rechten(self, gebruiker_id, allowed):
        self._rechten_overrides[gebruiker_id] = allowed

    def link_archivaris_aan_vernietigingstaak(self, gebruiker_id, taak_id):
        if gebruiker_id not in self._gebruikers:
            raise GebruikerNietGevondenException()
        if taak_id not in self._vernietigingstaken:
            raise VernietigingstaakNietGevondenException()
        rechten = self._rechten_overrides.get(gebruiker_id, self._gebruikers[gebruiker_id]['rechten'])
        if not rechten:
            raise OnvoldoendeRechtenException()
        if (gebruiker_id, taak_id) in self._gekoppelde_archivarissen:
            raise ArchivarisAlGekoppeldException()
        self._gekoppelde_archivarissen.add((gebruiker_id, taak_id))
        return True

    def is_archivaris_gekopppeld(self, gebruiker_id, taak_id):
        return (gebruiker_id, taak_id) in self._gekoppelde_archivarissen