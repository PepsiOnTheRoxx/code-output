import pytest
from unittest.mock import patch, MagicMock
from src.services.boekread import BoekService
from src.services.boekread_exceptions import BoekNotFoundException, DatabaseException

@pytest.fixture
def boek_data():
    return {
        "id": 1,
        "titel": "De ontdekking van de hemel",
        "auteur": "Harry Mulisch",
        "jaar": 1992
    }

def test_get_boek_by_id_success(boek_data):
    with patch("src.services.boekread.BoekRepository") as MockRepo:
        instance = MockRepo.return_value
        instance.get_by_id.return_value = boek_data
        service = BoekService()
        result = service.get_boek_by_id(1)
        assert result["id"] == 1
        assert result["titel"] == "De ontdekking van de hemel"
        assert result["auteur"] == "Harry Mulisch"
        assert result["jaar"] == 1992
        instance.get_by_id.assert_called_once_with(1)

def test_get_boek_by_id_not_found():
    with patch("src.services.boekread.BoekRepository") as MockRepo:
        instance = MockRepo.return_value
        instance.get_by_id.side_effect = BoekNotFoundException("Boek niet gevonden")
        service = BoekService()
        with pytest.raises(BoekNotFoundException):
            service.get_boek_by_id(999)

def test_get_boek_by_id_database_error():
    with patch("src.services.boekread.BoekRepository") as MockRepo:
        instance = MockRepo.return_value
        instance.get_by_id.side_effect = DatabaseException("Database fout")
        service = BoekService()
        with pytest.raises(DatabaseException):
            service.get_boek_by_id(1)

def test_get_all_boeken_success(boek_data):
    with patch("src.services.boekread.BoekRepository") as MockRepo:
        instance = MockRepo.return_value
        instance.get_all.return_value = [boek_data]
        service = BoekService()
        result = service.get_all_boeken()
        assert isinstance(result, list)
        assert result[0]["id"] == 1
        assert result[0]["titel"] == boek_data["titel"]
        instance.get_all.assert_called_once()

def test_get_all_boeken_empty():
    with patch("src.services.boekread.BoekRepository") as MockRepo:
        instance = MockRepo.return_value
        instance.get_all.return_value = []
        service = BoekService()
        result = service.get_all_boeken()
        assert result == []
        instance.get_all.assert_called_once()

def test_get_all_boeken_database_error():
    with patch("src.services.boekread.BoekRepository") as MockRepo:
        instance = MockRepo.return_value
        instance.get_all.side_effect = DatabaseException("Database fout")
        service = BoekService()
        with pytest.raises(DatabaseException):
            service.get_all_boeken()