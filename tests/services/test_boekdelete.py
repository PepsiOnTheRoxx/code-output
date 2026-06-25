import pytest
from unittest.mock import patch, MagicMock
from src.services.boekdelete import BoekService
from src.services.boekdelete_exceptions import BoekNietGevondenException, BoekDeleteException

@pytest.fixture
def boek_service():
    return BoekService()

def test_verwijder_boek_succesvol(boek_service):
    boek_id = 1
    with patch.object(BoekService, 'find_boek_by_id', return_value=MagicMock()) as mock_find, \
         patch.object(BoekService, 'delete_boek', return_value=None) as mock_delete:
        boek_service.verwijder_boek(boek_id)
        mock_find.assert_called_once_with(boek_id)
        mock_delete.assert_called_once_with(boek_id)

def test_verwijder_boek_boek_niet_gevonden(boek_service):
    boek_id = 2
    with patch.object(BoekService, 'find_boek_by_id', return_value=None):
        with pytest.raises(BoekNietGevondenException):
            boek_service.verwijder_boek(boek_id)

def test_verwijder_boek_throws_delete_exception(boek_service):
    boek_id = 3
    with patch.object(BoekService, 'find_boek_by_id', return_value=MagicMock()), \
         patch.object(BoekService, 'delete_boek', side_effect=BoekDeleteException):
        with pytest.raises(BoekDeleteException):
            boek_service.verwijder_boek(boek_id)

def test_verwijder_boek_meerdere_calls(boek_service):
    boek_id = 4
    with patch.object(BoekService, 'find_boek_by_id', return_value=MagicMock()) as mock_find, \
         patch.object(BoekService, 'delete_boek', return_value=None) as mock_delete:
        for _ in range(3):
            boek_service.verwijder_boek(boek_id)
        assert mock_find.call_count == 3
        assert mock_delete.call_count == 3