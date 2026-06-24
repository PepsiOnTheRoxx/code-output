import pytest
from src.gebruikerservice import GebruikerService, GebruikerNotFoundException

@pytest.fixture
def gebruiker_service():
    return GebruikerService()

def test_read_gebruiker_returns_details(gebruiker_service):
    gebruiker_id = 1
    gebruiker_service.add_gebruiker(gebruiker_id, "Jan Jansen", "jan.jansen@email.com")
    result = gebruiker_service.read_gebruiker(gebruiker_id)
    assert result["Naam"] == "Jan Jansen"
    assert result["Emailadres"] == "jan.jansen@email.com"

def test_read_gebruiker_not_found(gebruiker_service):
    gebruiker_id = 999
    with pytest.raises(GebruikerNotFoundException):
        gebruiker_service.read_gebruiker(gebruiker_id)

def test_read_gebruiker_multiple_gebruikers(gebruiker_service):
    gebruiker_service.add_gebruiker(1, "Jan Jansen", "jan.jansen@email.com")
    gebruiker_service.add_gebruiker(2, "Piet Pietersen", "piet.pietersen@email.com")
    result1 = gebruiker_service.read_gebruiker(1)
    result2 = gebruiker_service.read_gebruiker(2)
    assert result1["Naam"] == "Jan Jansen"
    assert result1["Emailadres"] == "jan.jansen@email.com"
    assert result2["Naam"] == "Piet Pietersen"
    assert result2["Emailadres"] == "piet.pietersen@email.com"

def test_read_gebruiker_email_is_correct(gebruiker_service):
    gebruiker_service.add_gebruiker(3, "Anna de Boer", "anna.deboer@email.com")
    result = gebruiker_service.read_gebruiker(3)
    assert result["Emailadres"].endswith("@email.com")