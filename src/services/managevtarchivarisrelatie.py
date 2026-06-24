from src.services.managevtarchivarisrelatie_exceptions import (
    ArchivarisAlreadyExistsException,
    ArchivarisRelationNotFoundException,
    UserNotFoundException,
    VernietigingstaakNotFoundException
)

# Simpele in-memory datastore voor demonstratie-/testdoeleinden
USERS = {}
TAKEN = {}
ARCHIVARIS_RELATIES = set()  # Set van (user_id, taak_id) tuples

class User:
    def __init__(self, id):
        self.id = id

class Taak:
    def __init__(self, id):
        self.id = id

class VTArchivarisRelatieService:
    @property
    def ARCHIVARIS_RELATIES(self):
        # property voor tests die .ARCHIVARIS_RELATIES verwachten
        global ARCHIVARIS_RELATIES
        return ARCHIVARIS_RELATIES
    def add_archivaris(self, user_id, taak_id):
        user = self.get_user_by_id(user_id)
        taak = self.get_vernietigingstaak_by_id(taak_id)
        if self.is_user_archivaris_of_taak(user_id, taak_id):
            raise ArchivarisAlreadyExistsException()
        self.add_archivaris_relation(user_id, taak_id)

    def remove_archivaris(self, user_id, taak_id):
        if not self.is_user_archivaris_of_taak(user_id, taak_id):
            raise ArchivarisRelationNotFoundException()
        self.remove_archivaris_relation(user_id, taak_id)

    def get_archivarissen_for_taak(self, taak_id):
        self.get_vernietigingstaak_by_id(taak_id)
        return self.get_archivarissen_by_taak_id(taak_id)

    def get_user_by_id(self, user_id):
        global USERS
        if user_id in USERS:
            return USERS[user_id]
        raise UserNotFoundException()

    def get_vernietigingstaak_by_id(self, taak_id):
        global TAKEN
        if taak_id in TAKEN:
            return TAKEN[taak_id]
        raise VernietigingstaakNotFoundException()

    def is_user_archivaris_of_taak(self, user_id, taak_id):
        global ARCHIVARIS_RELATIES
        return (user_id, taak_id) in ARCHIVARIS_RELATIES

    def add_archivaris_relation(self, user_id, taak_id):
        global ARCHIVARIS_RELATIES
        ARCHIVARIS_RELATIES.add((user_id, taak_id))

    def remove_archivaris_relation(self, user_id, taak_id):
        global ARCHIVARIS_RELATIES
        ARCHIVARIS_RELATIES.discard((user_id, taak_id))

    def get_archivarissen_by_taak_id(self, taak_id):
        global ARCHIVARIS_RELATIES
        result = []
        for (uid, tid) in ARCHIVARIS_RELATIES:
            if tid == taak_id:
                result.append(self.get_user_by_id(uid))
        return result
