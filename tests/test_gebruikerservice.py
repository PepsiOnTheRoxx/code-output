import pytest
from src.gebruikerservice import GebruikerService, Gebruiker

class TestGebruikerService:

    @pytest.fixture
    def gebruiker_service(self):
        return GebruikerService()

    def test_creeer_gebruiker_correct(self, gebruiker_service):
        gebruiker_data = {"naam": "Jan", "email": "jan@example.com"}
        gebruiker = gebruiker_service.creeer_gebruiker(gebruiker_data)

        assert gebruiker is not None
        assert isinstance(gebruiker, Gebruiker)
        assert gebruiker.naam == "Jan"
        assert gebruiker.email == "jan@example.com"

    def test_creeer_gebruiker_zonder_naam(self, gebruiker_service):
        gebruiker_data = {"email": "jan@example.com"}
        with pytest.raises(ValueError, match="Naam is verplicht"):
            gebruiker_service.creeer_gebruiker(gebruiker_data)

    def test_creeer_gebruiker_zonder_email(self, gebruiker_service):
        gebruiker_data = {"naam": "Jan"}
        with pytest.raises(ValueError, match="Email is verplicht"):
            gebruiker_service.creeer_gebruiker(gebruiker_data)

    def test_creeer_gebruiker_met_ongedeldig_email(self, gebruiker_service):
        gebruiker_data = {"naam": "Jan", "email": "ongeldig_email"}
        with pytest.raises(ValueError, match="Ongeldig emailadres"):
            gebruiker_service.creeer_gebruiker(gebruiker_data)

    def test_gebruiker_service_opslaan(self, gebruiker_service):
        gebruiker_data = {"naam": "Jan", "email": "jan@example.com"}
        gebruiker_service.creeer_gebruiker(gebruiker_data)
        assert len(gebruiker_service.gebruikers) == 1

    def test_gebruiker_service_dubbele_email(self, gebruiker_service):
        gebruiker_data1 = {"naam": "Jan", "email": "jan@example.com"}
        gebruiker_data2 = {"naam": "Piet", "email": "jan@example.com"}
        gebruiker_service.creeer_gebruiker(gebruiker_data1)

        with pytest.raises(ValueError, match="Email moet uniek zijn"):
            gebruiker_service.creeer_gebruiker(gebruiker_data2)