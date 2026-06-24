import pytest
from unittest.mock import patch, MagicMock
from src.services.managevtbronnenrelatie import VTBronnenRelatieService
from src.services.managevtbronnenrelatie_exceptions import VTBronnenRelatieNotFoundException, VTBronnenRelatieAlreadyExistsException, VTBronnenRelatieUpdateException

def test_create_vtbron_relatie_success():
    with patch('src.services.managevtbronnenrelatie.VTBronnenRelatieRepository') as mock_repo_cls:
        mock_repo = MagicMock()
        mock_repo_cls.return_value = mock_repo
        service = VTBronnenRelatieService()
        mock_repo.exists.return_value = False
        mock_repo.add.return_value = None

        result = service.create_relatie(vernietigingstaak_id=1, bron_id=2)

        mock_repo.exists.assert_called_once_with(vernietigingstaak_id=1, bron_id=2)
        mock_repo.add.assert_called_once_with(vernietigingstaak_id=1, bron_id=2)
        assert result is True

def test_create_vtbron_relatie_already_exists():
    with patch('src.services.managevtbronnenrelatie.VTBronnenRelatieRepository') as mock_repo_cls:
        mock_repo = MagicMock()
        mock_repo_cls.return_value = mock_repo
        service = VTBronnenRelatieService()
        mock_repo.exists.return_value = True

        with pytest.raises(VTBronnenRelatieAlreadyExistsException):
            service.create_relatie(vernietigingstaak_id=1, bron_id=2)

def test_delete_vtbron_relatie_success():
    with patch('src.services.managevtbronnenrelatie.VTBronnenRelatieRepository') as mock_repo_cls:
        mock_repo = MagicMock()
        mock_repo_cls.return_value = mock_repo
        mock_repo.exists.return_value = True
        mock_repo.delete.return_value = None
        service = VTBronnenRelatieService()
        
        result = service.delete_relatie(vernietigingstaak_id=1, bron_id=2)

        mock_repo.exists.assert_called_once_with(vernietigingstaak_id=1, bron_id=2)
        mock_repo.delete.assert_called_once_with(vernietigingstaak_id=1, bron_id=2)
        assert result is True

def test_delete_vtbron_relatie_not_found():
    with patch('src.services.managevtbronnenrelatie.VTBronnenRelatieRepository') as mock_repo_cls:
        mock_repo = MagicMock()
        mock_repo_cls.return_value = mock_repo
        mock_repo.exists.return_value = False
        service = VTBronnenRelatieService()

        with pytest.raises(VTBronnenRelatieNotFoundException):
            service.delete_relatie(vernietigingstaak_id=1, bron_id=3)

def test_update_vtbron_relatie_success():
    with patch('src.services.managevtbronnenrelatie.VTBronnenRelatieRepository') as mock_repo_cls:
        mock_repo = MagicMock()
        mock_repo_cls.return_value = mock_repo
        mock_repo.exists.return_value = True
        mock_repo.update.return_value = None
        service = VTBronnenRelatieService()

        result = service.update_relatie(vernietigingstaak_id=1, bron_id=2, nieuwe_bron_id=5)

        mock_repo.exists.assert_called_with(vernietigingstaak_id=1, bron_id=2)
        mock_repo.update.assert_called_once_with(vernietigingstaak_id=1, bron_id=2, nieuwe_bron_id=5)
        assert result is True

def test_update_vtbron_relatie_not_found():
    with patch('src.services.managevtbronnenrelatie.VTBronnenRelatieRepository') as mock_repo_cls:
        mock_repo = MagicMock()
        mock_repo_cls.return_value = mock_repo
        mock_repo.exists.return_value = False
        service = VTBronnenRelatieService()

        with pytest.raises(VTBronnenRelatieNotFoundException):
            service.update_relatie(vernietigingstaak_id=1, bron_id=3, nieuwe_bron_id=4)

def test_update_vtbron_relatie_failure():
    with patch('src.services.managevtbronnenrelatie.VTBronnenRelatieRepository') as mock_repo_cls:
        mock_repo = MagicMock()
        mock_repo_cls.return_value = mock_repo
        mock_repo.exists.return_value = True
        mock_repo.update.side_effect = VTBronnenRelatieUpdateException()
        service = VTBronnenRelatieService()

        with pytest.raises(VTBronnenRelatieUpdateException):
            service.update_relatie(vernietigingstaak_id=10, bron_id=11, nieuwe_bron_id=12)

def test_get_vtbronnen_by_taak_success():
    with patch('src.services.managevtbronnenrelatie.VTBronnenRelatieRepository') as mock_repo_cls:
        mock_repo = MagicMock()
        mock_repo_cls.return_value = mock_repo
        mock_repo.get_bronnen_by_taak.return_value = [2, 3, 5]
        service = VTBronnenRelatieService()

        bronnen = service.get_bronnen_by_taak(vernietigingstaak_id=1)

        mock_repo.get_bronnen_by_taak.assert_called_once_with(vernietigingstaak_id=1)
        assert bronnen == [2, 3, 5]

def test_get_vtbronnen_by_taak_empty():
    with patch('src.services.managevtbronnenrelatie.VTBronnenRelatieRepository') as mock_repo_cls:
        mock_repo = MagicMock()
        mock_repo_cls.return_value = mock_repo
        mock_repo.get_bronnen_by_taak.return_value = []
        service = VTBronnenRelatieService()

        bronnen = service.get_bronnen_by_taak(vernietigingstaak_id=42)

        mock_repo.get_bronnen_by_taak.assert_called_once_with(vernietigingstaak_id=42)
        assert bronnen == []
