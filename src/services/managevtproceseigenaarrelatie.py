from src.services.managevtproceseigenaarrelatie_exceptions import (
    VTProceseigenaarAlBestaandException,
    VTProceseigenaarNietGevondenException,
    VerbodenWijzigingException
)

class VTProceseigenaarRelatieService:
    def toevoegen_proceseigenaar(self, gebruiker_id, vernietigingstaak_id):
        if self.bestaat_relatie(gebruiker_id, vernietigingstaak_id):
            raise VTProceseigenaarAlBestaandException()
        self.opslaan_relatie(gebruiker_id, vernietigingstaak_id)

    def verwijderen_proceseigenaar(self, gebruiker_id, vernietigingstaak_id):
        if not self.bestaat_relatie(gebruiker_id, vernietigingstaak_id):
            raise VTProceseigenaarNietGevondenException()
        self.verwijder_relatie(gebruiker_id, vernietigingstaak_id)

    def wijzig_proceseigenaar(self, gebruiker_id, vernietigingstaak_id, nieuwe_gebruiker_id):
        if not self.is_wijziging_toegestaan(gebruiker_id, vernietigingstaak_id, nieuwe_gebruiker_id):
            raise VerbodenWijzigingException()
        self.update_relatie(gebruiker_id, vernietigingstaak_id, nieuwe_gebruiker_id)

    def raadpleeg_proceseigenaar(self, vernietigingstaak_id):
        proceseigenaar = self.get_proceseigenaar_by_vernietigingstaak(vernietigingstaak_id)
        if proceseigenaar is None:
            raise VTProceseigenaarNietGevondenException()
        return proceseigenaar

    # onderstaande methoden moeten worden voorzien van daadwerkelijke implementatie in bijv. repository of ORM laag

    def bestaat_relatie(self, gebruiker_id, vernietigingstaak_id):
        # zou query naar DB of datalaag zijn
        raise NotImplementedError()

    def opslaan_relatie(self, gebruiker_id, vernietigingstaak_id):
        # zou insert-query of save aanroepen
        raise NotImplementedError()

    def verwijder_relatie(self, gebruiker_id, vernietigingstaak_id):
        # zou verwijder-operatie aanroepen in DB/datalaag
        raise NotImplementedError()

    def is_wijziging_toegestaan(self, gebruiker_id, vernietigingstaak_id, nieuwe_gebruiker_id):
        # controle businessrules
        raise NotImplementedError()

    def update_relatie(self, gebruiker_id, vernietigingstaak_id, nieuwe_gebruiker_id):
        # zou update-operatie aanroepen
        raise NotImplementedError()

    def get_proceseigenaar_by_vernietigingstaak(self, vernietigingstaak_id):
        # zou query doen naar proceseigenaar
        raise NotImplementedError()