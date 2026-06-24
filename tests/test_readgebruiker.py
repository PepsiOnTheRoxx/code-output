import pytest
from src.readgebruiker import UserService, GebruikerNotFoundException

@pytest.fixture
def gebruiker_data():
    return [
        {"id": 1, "naam": "Jan Jansen", "email": "jan@example.com"},
        {"id": 2, "naam": "Piet Pieters", "email": "piet@example.com"},
        {"id": 3, "naam": "Klaas Klaassen", "email": "klaas@example.com"}
    ]

@pytest.fixture
def user_service(gebruiker_data):
    service = UserService(gebruiker_data)
    return service

def test_read_existing_gebruiker_by_id(user_service):
    gebruiker = user_service.read_gebruiker(1)
    assert gebruiker["id"] == 1
    assert gebruiker["naam"] == "Jan Jansen"
    assert gebruiker["email"] == "jan@example.com"

def test_read_another_existing_gebruiker_by_id(user_service):
    gebruiker = user_service.read_gebruiker(2)
    assert gebruiker["id"] == 2
    assert gebruiker["naam"] == "Piet Pieters"
    assert gebruiker["email"] == "piet@example.com"

def test_read_non_existing_gebruiker_raises(user_service):
    with pytest.raises(GebruikerNotFoundException):
        user_service.read_gebruiker(99)

def test_read_gebruiker_returns_copy_not_reference(user_service, gebruiker_data):
    gebruiker = user_service.read_gebruiker(1)
    gebruiker["naam"] = "Andere Naam"
    orig_gebruiker = next(g for g in gebruiker_data if g["id"] == 1)
    assert orig_gebruiker["naam"] == "Jan Jansen"
    assert gebruiker["naam"] == "Andere Naam"
    assert orig_gebruiker["naam"] != gebruiker["naam"]

def test_read_gebruiker_with_invalid_id_type_raises(user_service):
    with pytest.raises(TypeError):
        user_service.read_gebruiker("one")