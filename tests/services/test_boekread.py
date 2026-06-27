import pytest
from unittest.mock import patch, MagicMock
from src.services.boekread import BoekService
from src.services.boekread_exceptions import BoekNietGevondenException

def test_get_boek_by_id_bestaat():
    mock_boek = MagicMock()
    with patch("src.services.boekread.BoekRepository") as MockRepo:
        instance = MockRepo.return_value
        instance.get_by_id.return_value = mock_boek
        service = BoekService()
        result = service.get_boek_by_id(1)
        assert result == mock_boek
        instance.get_by_id.assert_called_once_with(1)

def test_get_boek_by_id_bestaat_niet():
    with patch("src.services.boekread.BoekRepository") as MockRepo:
        instance = MockRepo.return_value
        instance.get_by_id.return_value = None
        service = BoekService()
        with pytest.raises(BoekNietGevondenException):
            service.get_boek_by_id(99)
        instance.get_by_id.assert_called_once_with(99)

def test_get_all_boeken_levert_lijst():
    mock_boeken = [MagicMock(), MagicMock()]
    with patch("src.services.boekread.BoekRepository") as MockRepo:
        instance = MockRepo.return_value
        instance.get_all.return_value = mock_boeken
        service = BoekService()
        result = service.get_all_boeken()
        assert result == mock_boeken
        instance.get_all.assert_called_once()

def test_get_all_boeken_leeg():
    with patch("src.services.boekread.BoekRepository") as MockRepo:
        instance = MockRepo.return_value
        instance.get_all.return_value = []
        service = BoekService()
        result = service.get_all_boeken()
        assert result == []
        instance.get_all.assert_called_once()

def test_get_boek_by_id_exception_raised():
    with patch("src.services.boekread.BoekRepository") as MockRepo:
        instance = MockRepo.return_value
        instance.get_by_id.side_effect = Exception("Database fout")
        service = BoekService()
        with pytest.raises(Exception) as exc_info:
            service.get_boek_by_id(1)
        assert "Database fout" in str(exc_info.value)
        instance.get_by_id.assert_called_once_with(1)