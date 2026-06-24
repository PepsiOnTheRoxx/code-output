from src.services.managevtarchivarisrelatie_exceptions import (
    ArchivarisAlreadyExistsException,
    ArchivarisRelationNotFoundException,
    UserNotFoundException,
    VernietigingstaakNotFoundException
)

class VTArchivarisRelatieService:
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

    # Stub methods, to be implemented in subclass or via patching in tests
    def get_user_by_id(self, user_id):
        raise NotImplementedError

    def get_vernietigingstaak_by_id(self, taak_id):
        raise NotImplementedError

    def is_user_archivaris_of_taak(self, user_id, taak_id):
        raise NotImplementedError

    def add_archivaris_relation(self, user_id, taak_id):
        raise NotImplementedError

    def remove_archivaris_relation(self, user_id, taak_id):
        raise NotImplementedError

    def get_archivarissen_by_taak_id(self, taak_id):
        raise NotImplementedError
