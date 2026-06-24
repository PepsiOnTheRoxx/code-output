class Gebruiker:
    def __init__(self, gebruiker_id, naam):
        self.gebruiker_id = gebruiker_id
        self.naam = naam

class Vernietigingstaak:
    def __init__(self, taak_id, omschrijving):
        self.taak_id = taak_id
        self.omschrijving = omschrijving
        self.proceseigenaar = None

class ProceseigenaarAlreadyAssignedException(Exception):
    pass

class ProceseigenaarNotAssignedException(Exception):
    pass

class VTProceseigenaarRelation:
    def __init__(self):
        # Key: vernietigingstaak_id, Value: gebruiker instance
        self.taak_proceseigenaar = {}

    def koppel_proceseigenaar(self, gebruiker, vernietigingstaak):
        if vernietigingstaak.taak_id in self.taak_proceseigenaar:
            raise ProceseigenaarAlreadyAssignedException(
                f"Taak {vernietigingstaak.taak_id} heeft al een proceseigenaar."
            )
        self.taak_proceseigenaar[vernietigingstaak.taak_id] = gebruiker
        vernietigingstaak.proceseigenaar = gebruiker

    def ontkoppel_proceseigenaar(self, vernietigingstaak):
        if vernietigingstaak.taak_id not in self.taak_proceseigenaar:
            raise ProceseigenaarNotAssignedException(
                f"Er is geen proceseigenaar gekoppeld aan taak {vernietigingstaak.taak_id}."
            )
        del self.taak_proceseigenaar[vernietigingstaak.taak_id]
        vernietigingstaak.proceseigenaar = None

    def get_proceseigenaar(self, vernietigingstaak):
        return self.taak_proceseigenaar.get(vernietigingstaak.taak_id, None)

class DestructionTaskService:
    def __init__(self):
        self.vt_relation = VTProceseigenaarRelation()

    def wijs_proceseigenaar_toe(self, gebruiker, vernietigingstaak):
        self.vt_relation.koppel_proceseigenaar(gebruiker, vernietigingstaak)

    def verwijder_proceseigenaar(self, vernietigingstaak):
        self.vt_relation.ontkoppel_proceseigenaar(vernietigingstaak)

    def proceseigenaar_ophalen(self, vernietigingstaak):
        return self.vt_relation.get_proceseigenaar(vernietigingstaak)