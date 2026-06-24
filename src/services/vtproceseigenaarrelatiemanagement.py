from src.services.vtproceseigenaarrelatiemanagement_exceptions import (
    VTProceseigenaarRelatieAlreadyExistsException,
    VTProceseigenaarRelatieNotFoundException
)

class VTProceseigenaarRelatieService:
    def __init__(self):
        self._relaties = {}  # {vernietigingstaak_id: set(gebruiker_id)}

    def koppel_proceseigenaar(self, vernietigingstaak_id, gebruiker_id):
        if vernietigingstaak_id not in self._relaties:
            self._relaties[vernietigingstaak_id] = set()
        if gebruiker_id in self._relaties[vernietigingstaak_id]:
            raise VTProceseigenaarRelatieAlreadyExistsException()
        self._relaties[vernietigingstaak_id].add(gebruiker_id)

    def verwijder_proceseigenaar_relatie(self, vernietigingstaak_id, gebruiker_id):
        if (
            vernietigingstaak_id not in self._relaties or
            gebruiker_id not in self._relaties[vernietigingstaak_id]
        ):
            raise VTProceseigenaarRelatieNotFoundException()
        self._relaties[vernietigingstaak_id].remove(gebruiker_id)
        if not self._relaties[vernietigingstaak_id]:
            del self._relaties[vernietigingstaak_id]

    def is_proceseigenaar(self, vernietigingstaak_id, gebruiker_id):
        return (
            vernietigingstaak_id in self._relaties and
            gebruiker_id in self._relaties[vernietigingstaak_id]
        )

    def lijst_proceseigenaars(self, vernietigingstaak_id):
        if vernietigingstaak_id in self._relaties:
            return list(self._relaties[vernietigingstaak_id])
        return []
