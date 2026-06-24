class VernietigingstaakNotFound(Exception):
    pass

# Alias zodat de tests het juiste exceptiontype vinden
VernietigingstaakNotFoundException = VernietigingstaakNotFound

class Vernietigingstaak:
    def __init__(self, id, naam):
        self.id = id
        self.naam = naam

class DestructionTaskService:
    def __init__(self, vernietigingstaken=None):
        if vernietigingstaken is None:
            self.vernietigingstaken = []
        else:
            self.vernietigingstaken = list(vernietigingstaken)

    def delete_vernietigingstaak(self, taak_id):
        for i, taak in enumerate(self.vernietigingstaken):
            if taak.id == taak_id:
                del self.vernietigingstaken[i]
                return True
        raise VernietigingstaakNotFound(f"Vernietigingstaak met id {taak_id} niet gevonden.")