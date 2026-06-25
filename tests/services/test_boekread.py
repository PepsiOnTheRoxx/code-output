import pytest
from unittest.mock import patch, MagicMock
from src.services.boekread import BoekService
from src.services.boekread_exceptions import BoekNotFoundException

@pytest.fixture
def boek_data():
    return {
        "id": 1,
        "titel": "De Donkere Kamer van Damokles",
        "auteur": "W.F. Hermans",
        "isbn": "9789023451235"
    }

@pytest.fixture
def boek_lijst_data():
    return [
        {"id": 1, "titel": "De Donkere Kamer van Damokles", "auteur": "W.F. Hermans", "isbn": "9789023451235"},
        {"id": 2, "titel": "Max Havelaar", "auteur": "Multatuli", "isbn": "9789023456789"},
    ]

@patch("src.services.boekread.BoekRepository")
def test_lees_boek_by_id_succes(mock_boek_repo, boek_data):
    instance = mock_boek_repo.return_value
    instance.get_boek_by_id.return_value = boek_data
    service = BoekService()
    result = service.lees_boek_by_id(1)
    assert result == boek_data
    instance.get_boek_by_id.assert_called_once_with(1)

@patch("src.services.boekread.BoekRepository")
def test_lees_boek_by_id_niet_gevonden(mock_boek_repo):
    instance = mock_boek_repo.return_value
    instance.get_boek_by_id.return_value = None
    service = BoekService()
    with pytest.raises(BoekNotFoundException):
        service.lees_boek_by_id(999)

@patch("src.services.boekread.BoekRepository")
def test_lees_alle_boeken_succes(mock_boek_repo, boek_lijst_data):
    instance = mock_boek_repo.return_value
    instance.get_all_boeken.return_value = boek_lijst_data
    service = BoekService()
    result = service.lees_alle_boeken()
    assert result == boek_lijst_data
    instance.get_all_boeken.assert_called_once_with()

@patch("src.services.boekread.BoekRepository")
def test_lees_alle_boeken_leeg(mock_boek_repo):
    instance = mock_boek_repo.return_value
    instance.get_all_boeken.return_value = []
    service = BoekService()
    result = service.lees_alle_boeken()
    assert result == []
    instance.get_all_boeken.assert_called_once_with()

@patch("src.services.boekread.BoekRepository")
def test_lees_boek_by_id_raises_on_error(mock_boek_repo):
    instance = mock_boek_repo.return_value
    instance.get_boek_by_id.side_effect = Exception("Database error")
    service = BoekService()
    with pytest.raises(Exception) as exc_info:
        service.lees_boek_by_id(1)
    assert "Database error" in str(exc_info.value)

@patch("src.services.boekread.BoekRepository")
def test_lees_alle_boeken_raises_on_error(mock_boek_repo):
    instance = mock_boek_repo.return_value
    instance.get_all_boeken.side_effect = Exception("Repository error")
    service = BoekService()
    with pytest.raises(Exception) as exc_info:
        service.lees_alle_boeken()
    assert "Repository error" in str(exc_info.value)
