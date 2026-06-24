import pytest
from unittest.mock import patch, MagicMock
from src.services.vtbronnenrelatie import VTBronnenRelatieService, reset_stores, BronRepository, VernietigingstaakRepository
from src.services.vtbronnenrelatie_exceptions import BronNotFoundException, VernietigingstaakNotFoundException, RelatieBestaatAlException

@pytest.fixture(autouse=True)
def clear_datastores():
    reset_stores()
    yield
    reset_stores()

@pytest.fixture
def service():
    return VTBronnenRelatieService()

@patch('src.services.vtbronnenrelatie.BronRepository')
@patch('src.services.vtbronnenrelatie.VernietigingstaakRepository')
@patch('src.services.vtbronnenrelatie.RelatieRepository')
def test_koppel_bron_aan_vernietigingstaak_succes(mock_relatie_repo, mock_vernietigingstaak_repo, mock_bron_repo, service):
    bron_id = 1
    taak_id = 10

    mock_bron_repo.return_value.get_by_id.return_value = MagicMock(id=bron_id)
    mock_vernietigingstaak_repo.return_value.get_by_id.return_value = MagicMock(id=taak_id)
    mock_relatie_repo.return_value.get_by_bron_en_taak.return_value = None

    service.bron_repo = mock_bron_repo.return_value
    service.vernietigingstaak_repo = mock_vernietigingstaak_repo.return_value
    service.relatie_repo = mock_relatie_repo.return_value

    service.koppel_bron_aan_vernietigingstaak(bron_id, taak_id)

    service.relatie_repo.create.assert_called_once_with(bron_id, taak_id)

@patch('src.services.vtbronnenrelatie.BronRepository')
@patch('src.services.vtbronnenrelatie.VernietigingstaakRepository')
@patch('src.services.vtbronnenrelatie.RelatieRepository')
def test_koppel_bron_aan_vernietigingstaak_bron_niet_gevonden(mock_relatie_repo, mock_vernietigingstaak_repo, mock_bron_repo, service):
    bron_id = 2
    taak_id = 20

    mock_bron_repo.return_value.get_by_id.return_value = None

    service.bron_repo = mock_bron_repo.return_value
    service.vernietigingstaak_repo = mock_vernietigingstaak_repo.return_value
    service.relatie_repo = mock_relatie_repo.return_value

    with pytest.raises(BronNotFoundException):
        service.koppel_bron_aan_vernietigingstaak(bron_id, taak_id)

@patch('src.services.vtbronnenrelatie.BronRepository')
@patch('src.services.vtbronnenrelatie.VernietigingstaakRepository')
@patch('src.services.vtbronnenrelatie.RelatieRepository')
def test_koppel_bron_aan_vernietigingstaak_vernietigingstaak_niet_gevonden(mock_relatie_repo, mock_vernietigingstaak_repo, mock_bron_repo, service):
    bron_id = 3
    taak_id = 30

    mock_bron_repo.return_value.get_by_id.return_value = MagicMock(id=bron_id)
    mock_vernietigingstaak_repo.return_value.get_by_id.return_value = None

    service.bron_repo = mock_bron_repo.return_value
    service.vernietigingstaak_repo = mock_vernietigingstaak_repo.return_value
    service.relatie_repo = mock_relatie_repo.return_value

    with pytest.raises(VernietigingstaakNotFoundException):
        service.koppel_bron_aan_vernietigingstaak(bron_id, taak_id)

@patch('src.services.vtbronnenrelatie.BronRepository')
@patch('src.services.vtbronnenrelatie.VernietigingstaakRepository')
@patch('src.services.vtbronnenrelatie.RelatieRepository')
def test_koppel_bron_aan_vernietigingstaak_relatie_bestaat_al(mock_relatie_repo, mock_vernietigingstaak_repo, mock_bron_repo, service):
    bron_id = 4
    taak_id = 40

    mock_bron_repo.return_value.get_by_id.return_value = MagicMock(id=bron_id)
    mock_vernietigingstaak_repo.return_value.get_by_id.return_value = MagicMock(id=taak_id)
    mock_relatie_repo.return_value.get_by_bron_en_taak.return_value = MagicMock()

    service.bron_repo = mock_bron_repo.return_value
    service.vernietigingstaak_repo = mock_vernietigingstaak_repo.return_value
    service.relatie_repo = mock_relatie_repo.return_value

    with pytest.raises(RelatieBestaatAlException):
        service.koppel_bron_aan_vernietigingstaak(bron_id, taak_id)

@patch('src.services.vtbronnenrelatie.RelatieRepository')
def test_verwijder_relatie_succes(mock_relatie_repo, service):
    bron_id = 5
    taak_id = 50

    mock_relatie_repo.return_value.delete_by_bron_en_taak.return_value = True
    service.relatie_repo = mock_relatie_repo.return_value

    result = service.verwijder_relatie(bron_id, taak_id)

    assert result is True
    service.relatie_repo.delete_by_bron_en_taak.assert_called_once_with(bron_id, taak_id)

@patch('src.services.vtbronnenrelatie.RelatieRepository')
def test_verwijder_relatie_bestaat_niet(mock_relatie_repo, service):
    bron_id = 6
    taak_id = 60

    mock_relatie_repo.return_value.delete_by_bron_en_taak.return_value = False
    service.relatie_repo = mock_relatie_repo.return_value

    result = service.verwijder_relatie(bron_id, taak_id)

    assert result is False
    service.relatie_repo.delete_by_bron_en_taak.assert_called_once_with(bron_id, taak_id)

@patch('src.services.vtbronnenrelatie.RelatieRepository')
def test_haal_op_relatie(mock_relatie_repo, service):
    bron_id = 7
    taak_id = 70

    relatie_obj = MagicMock(bron_id=bron_id, taak_id=taak_id)
    mock_relatie_repo.return_value.get_by_bron_en_taak.return_value = relatie_obj
    service.relatie_repo = mock_relatie_repo.return_value

    result = service.haal_op_relatie(bron_id, taak_id)

    assert result == relatie_obj
    service.relatie_repo.get_by_bron_en_taak.assert_called_once_with(bron_id, taak_id)

@patch('src.services.vtbronnenrelatie.RelatieRepository')
def test_haal_op_relatie_bestaat_niet(mock_relatie_repo, service):
    bron_id = 8
    taak_id = 80

    mock_relatie_repo.return_value.get_by_bron_en_taak.return_value = None
    service.relatie_repo = mock_relatie_repo.return_value

    result = service.haal_op_relatie(bron_id, taak_id)

    assert result is None
    service.relatie_repo.get_by_bron_en_taak.assert_called_once_with(bron_id, taak_id)
