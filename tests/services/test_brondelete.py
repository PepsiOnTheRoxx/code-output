import pytest
from unittest.mock import MagicMock, patch
from src.services.brondelete import BronService
from src.services.brondelete_exceptions import BronNotFoundException, BronDeleteException

@pytest.fixture
def bron_service():
    service = BronService()
    # Vul een paar "bronnen" voor testdoeleinden
    service._bronnen[12] = {"id": 12}
    service._bronnen[13] = {"id": 13}
    return service

def test_verwijdert_bestaande_bron(bron_service):
    bron_id = 12
    with patch.object(bron_service, "get_bron_by_id", return_value={"id": bron_id}) as mock_get_bron, \
         patch.object(bron_service, "delete_bron_by_id") as mock_delete_bron:
        bron_service.delete_bron(bron_id)
        mock_get_bron.assert_called_once_with(bron_id)
        mock_delete_bron.assert_called_once_with(bron_id)

def test_verwijder_bron_niet_gevonden(bron_service):
    bron_id = 999
    with patch.object(bron_service, "get_bron_by_id", return_value=None):
        with pytest.raises(BronNotFoundException):
            bron_service.delete_bron(bron_id)

def test_verwijder_bron_delete_exception(bron_service):
    bron_id = 12
    with patch.object(bron_service, "get_bron_by_id", return_value={"id": bron_id}), \
         patch.object(bron_service, "delete_bron_by_id", side_effect=BronDeleteException):
        with pytest.raises(BronDeleteException):
            bron_service.delete_bron(bron_id)
            
def test_delete_bron_roept_delete_bron_by_id(bron_service):
    bron_id = 12
    with patch.object(bron_service, "get_bron_by_id", return_value={"id": bron_id}), \
         patch.object(bron_service, "delete_bron_by_id") as mock_delete:
        bron_service.delete_bron(bron_id)
        mock_delete.assert_called_once_with(bron_id)

def test_delete_bron_multiple_calls(bron_service):
    bron_id_1 = 12
    bron_id_2 = 13
    with patch.object(bron_service, "get_bron_by_id", side_effect=[{"id": bron_id_1}, {"id": bron_id_2}]), \
         patch.object(bron_service, "delete_bron_by_id") as mock_delete:
        bron_service.delete_bron(bron_id_1)
        bron_service.delete_bron(bron_id_2)
        assert mock_delete.call_count == 2
        mock_delete.assert_any_call(bron_id_1)
        mock_delete.assert_any_call(bron_id_2)

# Extra integratietests op de real (niet gemockte) methods

def test_integreer_verwijdert_bestaande_bron():
    service = BronService()
    service._bronnen[123] = {"id": 123}
    service.delete_bron(123)
    assert 123 not in service._bronnen

def test_integreer_verwijder_nonexistent_bron():
    service = BronService()
    with pytest.raises(BronNotFoundException):
        service.delete_bron(99999)
