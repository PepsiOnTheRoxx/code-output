from src.services.boekupdate_exceptions import (
    BoekNotFoundException,
    BoekUpdateValidationException
)

class BoekService:
    VALID_BOEK_VELDEN = {'titel', 'auteur'}  # Uitbreidbaar met meerdere boekvelden

    def __init__(self, boek_repository):
        self.boek_repository = boek_repository

    def update_boek(self, boek_id, nieuwe_data):
        bestaand_boek = self.boek_repository.get_boek_by_id(boek_id)
        if not bestaand_boek:
            raise BoekNotFoundException(f"Boek met id {boek_id} niet gevonden")

        for veld, waarde in nieuwe_data.items():
            if veld not in self.VALID_BOEK_VELDEN:
                continue  # Sla niet-boekvelden in nieuwe_data over
            if veld == 'titel':
                if not waarde or not isinstance(waarde, str):
                    raise BoekUpdateValidationException("Boektitel mag niet leeg zijn")
                setattr(bestaand_boek, 'titel', waarde)
            elif veld == 'auteur':
                if not waarde or not isinstance(waarde, str):
                    raise BoekUpdateValidationException("Auteur mag niet leeg zijn")
                setattr(bestaand_boek, 'auteur', waarde)
            # Op meer validaties/velden uitbreiden indien vereist
        try:
            self.boek_repository.save_boek(bestaand_boek)
        except Exception as exc:
            raise exc
