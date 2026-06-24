class VernietigingstaakService:
    def delete_vernietigingstaak(self, taak_id):
        if taak_id is None:
            raise TypeError("taak_id mag niet None zijn")
        taak = self._get_taak_by_id(taak_id)
        if taak is None:
            raise ValueError("Taak niet gevonden")
        deleted = self._delete_taak(taak_id)
        return deleted

    def _get_taak_by_id(self, taak_id):
        # Dummy implementatie, wordt gemocked in tests
        pass

    def _delete_taak(self, taak_id):
        # Dummy implementatie, wordt gemocked in tests
        pass