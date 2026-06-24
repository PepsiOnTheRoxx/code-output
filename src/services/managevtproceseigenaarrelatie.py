from src.services.managevtproceseigenaarrelatie_exceptions import (
    VTProceseigenaarAlBestaandException,
    VTProceseigenaarNietGevondenException,
    VerbodenWijzigingException
)

class VTProceseigenaarRelatieService:
    _relaties = []  # Klasse-variabele, lijst met dicts: {gebruiker_id, vernietigingstaak_id}

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

    def bestaat_relatie(self, gebruiker_id, vernietigingstaak_id):
        return any(
            relatie['gebruiker_id'] == gebruiker_id and relatie['vernietigingstaak_id'] == vernietigingstaak_id
            for relatie in self._relaties
        )

    def opslaan_relatie(self, gebruiker_id, vernietigingstaak_id):
        self._relaties.append({
            'gebruiker_id': gebruiker_id,
            'vernietigingstaak_id': vernietigingstaak_id
        })

    def verwijder_relatie(self, gebruiker_id, vernietigingstaak_id):
        self._relaties = [
            relatie for relatie in self._relaties
            if not (relatie['gebruiker_id'] == gebruiker_id and relatie['vernietigingstaak_id'] == vernietigingstaak_id)
        ]

    def is_wijziging_toegestaan(self, gebruiker_id, vernietigingstaak_id, nieuwe_gebruiker_id):
        # In deze eenvoudige implementatie: toegestaan als de oude relatie bestaat en de nieuwe nog niet
        oud_bestaat = self.bestaat_relatie(gebruiker_id, vernietigingstaak_id)
        nieuw_bestaat = self.bestaat_relatie(nieuwe_gebruiker_id, vernietigingstaak_id)
        return oud_bestaat and not nieuw_bestaat

    def update_relatie(self, gebruiker_id, vernietigingstaak_id, nieuwe_gebruiker_id):
        gevonden = False
        for relatie in self._relaties:
            if relatie['gebruiker_id'] == gebruiker_id and relatie['vernietigingstaak_id'] == vernietigingstaak_id:
                relatie['gebruiker_id'] = nieuwe_gebruiker_id
                gevonden = True
                break
        if not gevonden:
            raise VTProceseigenaarNietGevondenException()

    def get_proceseigenaar_by_vernietigingstaak(self, vernietigingstaak_id):
        for relatie in self._relaties:
            if relatie['vernietigingstaak_id'] == vernietigingstaak_id:
                # In een echte implementatie zou je gebruiker ophalen, nu simuleren als dict
                return {'id': relatie['gebruiker_id'], 'naam': f'Gebruiker {relatie["gebruiker_id"]}'}
        return None
