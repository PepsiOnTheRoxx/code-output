from src.services.vtbronnenrelatiemanagement_exceptions import (
    KoppelingBestaatAlException,
    KoppelingNietGevondenException,
    OngeldigeBronException,
    OngeldigeVernietigingstaakException
)

class VTBronnenRelatieService:

    def __init__(self):
        self._koppelingen = set()

    def koppeling_toevoegen(self, vernietigingstaak_id, bron_id):
        if vernietigingstaak_id is None or not isinstance(vernietigingstaak_id, int):
            raise OngeldigeVernietigingstaakException()
        if not isinstance(bron_id, int):
            raise OngeldigeBronException()
        key = (vernietigingstaak_id, bron_id)
        if key in self._koppelingen:
            raise KoppelingBestaatAlException()
        self._koppelingen.add(key)
        return {"vernietigingstaak_id": vernietigingstaak_id, "bron_id": bron_id}

    def koppeling_verwijderen(self, vernietigingstaak_id, bron_id):
        key = (vernietigingstaak_id, bron_id)
        if key not in self._koppelingen:
            raise KoppelingNietGevondenException()
        self._koppelingen.remove(key)

    def lijst_koppelingen(self, vernietigingstaak_id):
        if not isinstance(vernietigingstaak_id, int):
            return []
        result = []
        for vt_id, bron_id in self._koppelingen:
            if vt_id == vernietigingstaak_id:
                result.append({"vernietigingstaak_id": vt_id, "bron_id": bron_id})
        return result
