import re
from src.services.creategebruiker_exceptions import InvalidEmailException, DuplicateGebruikerException

class Gebruiker:
    def __init__(self, id, naam, email):
        self.id = id
        self.naam = naam
        self.email = email

class GebruikerRepository:
    def exists_by_email(self, email):
        raise NotImplementedError

    def save(self, gebruiker):
        raise NotImplementedError

class GebruikerService:
    def __init__(self, gebruiker_repository):
        self.gebruiker_repository = gebruiker_repository

    def create_gebruiker(self, naam, email):
        if not naam or not naam.strip():
            raise ValueError("Naam mag niet leeg zijn")
        if not email or not self._is_valid_email(email):
            raise InvalidEmailException("Ongeldig emailadres")
        if self.gebruiker_repository.exists_by_email(email):
            raise DuplicateGebruikerException("Emailadres bestaat al")
        gebruiker = Gebruiker(None, naam, email)
        saved_gebruiker = self.gebruiker_repository.save(gebruiker)
        return saved_gebruiker

    def _is_valid_email(self, email):
        pattern = r"^[^@]+@[^@]+\.[^@]+$"
        return re.match(pattern, email) is not None