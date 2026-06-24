from src.services.vtproceseigenaarrelatie_exceptions import (
    ProceseigenaarNietGevondenException,
    VernietigingstaakNietGevondenException,
    ProceseigenaarRelatieBestaatAlException,
    ProceseigenaarRelatieNietGevondenException,
)

class VTProceseigenaarRelatieService:
    def __init__(self):
        self._taak_proceseigenaren = {}
        self._gebruiker_taken = {}
        self._gebruikers = {1: "Piet", 2: "Klaas", 5: "Gebr5", 7: "Gebr7", 10: "Gebr10", 12: "Gebr12", 25: "Gebr25", 99: "Gebr99"}
        self._taken = {20: "Taak20", 30: "Taak30", 33: "Taak33", 50: "Taak50", 100: "Taak100", 101: "Taak A", 102: "Taak B", 12345: "NietBestaat"}

    def koppel_proceseigenaar(self, gebruiker_id, taak_id):
        if gebruiker_id not in self._gebruikers:
            raise ProceseigenaarNietGevondenException()
        if taak_id not in self._taken:
            raise VernietigingstaakNietGevondenException()
        if taak_id in self._taak_proceseigenaren and gebruiker_id in self._taak_proceseigenaren[taak_id]:
            raise ProceseigenaarRelatieBestaatAlException()
        self._taak_proceseigenaren.setdefault(taak_id, set()).add(gebruiker_id)
        self._gebruiker_taken.setdefault(gebruiker_id, set()).add(taak_id)
        return True

    def verwijder_proceseigenaarrelatie(self, gebruiker_id, taak_id):
        if taak_id not in self._taak_proceseigenaren or gebruiker_id not in self._taak_proceseigenaren[taak_id]:
            raise ProceseigenaarRelatieNietGevondenException()
        self._taak_proceseigenaren[taak_id].remove(gebruiker_id)
        if not self._taak_proceseigenaren[taak_id]:
            del self._taak_proceseigenaren[taak_id]
        self._gebruiker_taken[gebruiker_id].remove(taak_id)
        if not self._gebruiker_taken[gebruiker_id]:
            del self._gebruiker_taken[gebruiker_id]

    def get_proceseigenaren_voor_taak(self, taak_id):
        if taak_id not in self._taak_proceseigenaren:
            return []
        return [{'id': g_id, 'naam': self._gebruikers.get(g_id, f'Gebruiker {g_id}')} for g_id in self._taak_proceseigenaren[taak_id]]

    def get_taken_voor_proceseigenaar(self, gebruiker_id):
        if gebruiker_id not in self._gebruiker_taken:
            return []
        return [{'id': t_id, 'omschrijving': self._taken.get(t_id, f'Taak {t_id}')} for t_id in self._gebruiker_taken[gebruiker_id]]
