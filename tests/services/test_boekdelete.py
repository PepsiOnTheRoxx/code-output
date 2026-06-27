import pytest
from unittest.mock import patch, MagicMock
from src.services.boekdelete import BoekService
from src.services.boekdelete_exceptions import BoekNotFoundException, DeleteNotAllowedException

@patch("src.services.boekdelete.BoekRepository")
def test_delete_boek_succeeds(mock_boek_repo):
    mock_repo = mock_boek_repo.return_value
    mock_repo.get_by_id.return_value = MagicMock(id=10)
    service = BoekService()
    service._repository = mock_repo

    service.delete_boek(10)

    mock_repo.get_by_id.assert_called_once_with(10)
    mock_repo.delete.assert_called_once_with(10)

@patch("src.services.boekdelete.BoekRepository")
def test_delete_boek_not_found_raises_exception(mock_boek_repo):
    mock_repo = mock_boek_repo.return_value
    mock_repo.get_by_id.return_value = None
    service = BoekService()
    service._repository = mock_repo

    with pytest.raises(BoekNotFoundException):
        service.delete_boek(99)

    mock_repo.get_by_id.assert_called_once_with(99)
    mock_repo.delete.assert_not_called()

@patch("src.services.boekdelete.BoekRepository")
def test_delete_boek_not_allowed_raises_exception(mock_boek_repo):
    mock_repo = mock_boek_repo.return_value
    mock_repo.get_by_id.return_value = MagicMock(id=5)
    mock_repo.delete.side_effect = DeleteNotAllowedException("Delete not permitted")
    service = BoekService()
    service._repository = mock_repo

    with pytest.raises(DeleteNotAllowedException):
        service.delete_boek(5)

    mock_repo.get_by_id.assert_called_once_with(5)
    mock_repo.delete.assert_called_once_with(5)

@patch("src.services.boekdelete.BoekRepository")
def test_delete_boek_calls_delete_with_correct_id(mock_boek_repo):
    mock_repo = mock_boek_repo.return_value
    mock_boek = MagicMock(id=8)
    mock_repo.get_by_id.return_value = mock_boek
    service = BoekService()
    service._repository = mock_repo

    service.delete_boek(8)

    mock_repo.delete.assert_called_once_with(8)

@patch("src.services.boekdelete.BoekRepository")
def test_delete_boek_handles_multiple_deletes(mock_boek_repo):
    mock_repo = mock_boek_repo.return_value
    mock_repo.get_by_id.side_effect = [MagicMock(id=1), MagicMock(id=2)]
    service = BoekService()
    service._repository = mock_repo

    service.delete_boek(1)
    service.delete_boek(2)

    assert mock_repo.delete.call_count == 2
    mock_repo.delete.assert_any_call(1)
    mock_repo.delete.assert_any_call(2)