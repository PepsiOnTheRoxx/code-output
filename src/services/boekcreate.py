from src.services.boekcreate_exceptions import (
    BoekCreateAlreadyExistsException,
    BoekCreateDataInvalidException
)

class BoekService:
    def __init__(self, repository):
        self.repository = repository

    def create_boek(self, boek_data):
        if not isinstance(boek_data, dict):
            raise BoekCreateDataInvalidException("Boek data moet een dictionary zijn")
        if not boek_data.get("titel") or not boek_data.get("auteur"):
            raise BoekCreateDataInvalidException("Titel en auteur zijn verplicht")
        if self.repository.exists(boek_data):
            raise BoekCreateAlreadyExistsException("Boek bestaat al")
        try:
            nieuw_boek = self.repository.save(boek_data)
            return nieuw_boek
        except Exception as exc:
            raise exc
