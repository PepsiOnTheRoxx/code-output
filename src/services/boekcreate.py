from src.services.boekcreate_exceptions import (
    BoekAlreadyExistsException,
    InvalidBoekDataException
)

class BoekService:
    def __init__(self, repository):
        self.repository = repository

    def create_boek(self, boek_data):
        if not isinstance(boek_data, dict):
            raise InvalidBoekDataException("Boek data moet een dictionary zijn")
        if not boek_data.get("titel") or not boek_data.get("auteur"):
            raise InvalidBoekDataException("Titel en auteur zijn verplicht")
        if self.repository.exists(boek_data):
            raise BoekAlreadyExistsException("Boek bestaat al")
        try:
            nieuw_boek = self.repository.save(boek_data)
            return nieuw_boek
        except Exception as exc:
            raise exc