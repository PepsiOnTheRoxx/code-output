from src.services.boekupdate_exceptions import (
    BoekNietGevondenException,
    OngeldigeBoekDataException
)

class BoekService:
    def __init__(self, boek_repository):
        self.boek_repository = boek_repository

    def update_boek(self, boek_id, nieuwe_data):
        bestaand_boek = self.boek_repository.get_boek_by_id(boek_id)
        if not bestaand_boek:
            raise BoekNietGevondenException(f"Boek met id {boek_id} niet gevonden")
        if "titel" in nieuwe_data:
            if not nieuwe_data["titel"] or not isinstance(nieuwe_data["titel"], str):
                raise OngeldigeBoekDataException("Boektitel mag niet leeg zijn")
            bestaand_boek.titel = nieuwe_data["titel"]
        if "auteur" in nieuwe_data:
            if not nieuwe_data["auteur"] or not isinstance(nieuwe_data["auteur"], str):
                raise OngeldigeBoekDataException("Auteur mag niet leeg zijn")
            bestaand_boek.auteur = nieuwe_data["auteur"]
        try:
            self.boek_repository.save_boek(bestaand_boek)
        except Exception as exc:
            raise exc