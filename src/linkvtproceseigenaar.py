from src.linkvtproceseigenaar_exceptions import *

class VernietigingstaakRelatiesService:
    def __init__(self):
        self._gebruikers = set([1, 2, 3, 4])
        self._taken = set([100, 200, 300, 400])
        self._koppelingen = set()

    def koppel_proceseigenaar(self, gebruiker_id, vernietigingstaak_id):
        if gebruiker_id is None or vernietigingstaak_id is None:
            raise OngeldigeRelatieException()
        if gebruiker_id not in self._gebruikers:
            raise GebruikerNietGevondenException()
        if vernietigingstaak_id not in self._taken:
            raise TaakNietGevondenException()
        key = (gebruiker_id, vernietigingstaak_id)
        if key in self._koppelingen:
            raise ProceseigenaarAlGekoppeldException()
        self._koppelingen.add(key)
        return True

    def is_proceseigenaar(self, gebruiker_id, vernietigingstaak_id):
        return (gebruiker_id, vernietigingstaak_id) in self._koppelingen
