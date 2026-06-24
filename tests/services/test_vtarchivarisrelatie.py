import pytest
from unittest.mock import patch, MagicMock
from src.services.vtarchivarisrelatie import VTArchivarisRelatieService
from src.services.vtarchivarisrelatie_exceptions import (
    ArchivarisRelatieAlreadyExistsException,
    ArchivarisRelatieNotFoundException,
    InvalidGebruikerException,
    InvalidVernietigingstaakException,
)

@pytest.fixture
def service():
    return VTArchivarisRelatieService()

def test_maak_relatie_succes(service):
    gebruiker_id = 10
    taak_id = 20
    with patch("src.services.vtarchivarisrelatie.VTArchivarisRelatieOpslag") as MockOpslag:
        opslag_mock = MagicMock()
        MockOpslag.return_value = opslag_mock
        opslag_mock.bestaat_relatie.return_value = False
        service.ops = opslag_mock
        service.maak_relatie(gebruiker_id, taak_id)
        opslag_mock.opslaan_relatie.assert_called_once_with(gebruiker_id, taak_id)

def test_maak_relatie_bestaat_al(service):
    gebruiker_id = 10
    taak_id = 20
    with patch("src.services.vtarchivarisrelatie.VTArchivarisRelatieOpslag") as MockOpslag:
        opslag_mock = MagicMock()
        MockOpslag.return_value = opslag_mock
        opslag_mock.bestaat_relatie.return_value = True
        service.ops = opslag_mock
        with pytest.raises(ArchivarisRelatieAlreadyExistsException):
            service.maak_relatie(gebruiker_id, taak_id)

def test_verwijder_relatie_succes(service):
    gebruiker_id = 42
    taak_id = 24
    with patch("src.services.vtarchivarisrelatie.VTArchivarisRelatieOpslag") as MockOpslag:
        opslag_mock = MagicMock()
        MockOpslag.return_value = opslag_mock
        opslag_mock.bestaat_relatie.return_value = True
        service.ops = opslag_mock
        service.verwijder_relatie(gebruiker_id, taak_id)
        opslag_mock.verwijder_relatie.assert_called_once_with(gebruiker_id, taak_id)

def test_verwijder_relatie_niet_gevonden(service):
    gebruiker_id = 99
    taak_id = 101
    with patch("src.services.vtarchivarisrelatie.VTArchivarisRelatieOpslag") as MockOpslag:
        opslag_mock = MagicMock()
        MockOpslag.return_value = opslag_mock
        opslag_mock.bestaat_relatie.return_value = False
        service.ops = opslag_mock
        with pytest.raises(ArchivarisRelatieNotFoundException):
            service.verwijder_relatie(gebruiker_id, taak_id)

def test_alle_relatie_ids_per_gebruiker_leeg(service):
    gebruiker_id = 17
    with patch("src.services.vtarchivarisrelatie.VTArchivarisRelatieOpslag") as MockOpslag:
        opslag_mock = MagicMock()
        MockOpslag.return_value = opslag_mock
        opslag_mock.haal_taak_ids_voor_gebruiker.return_value = []
        service.ops = opslag_mock
        result = service.alle_relatie_ids_per_gebruiker(gebruiker_id)
        assert result == []

def test_alle_relatie_ids_per_gebruiker_met_resultaat(service):
    gebruiker_id = 25
    taken = [10, 11, 12]
    with patch("src.services.vtarchivarisrelatie.VTArchivarisRelatieOpslag") as MockOpslag:
        opslag_mock = MagicMock()
        MockOpslag.return_value = opslag_mock
        opslag_mock.haal_taak_ids_voor_gebruiker.return_value = taken
        service.ops = opslag_mock
        result = service.alle_relatie_ids_per_gebruiker(gebruiker_id)
        assert result == taken

def test_maak_relatie_invalid_gebruiker(service):
    gebruiker_id = "geen_int"
    taak_id = 4
    with pytest.raises(InvalidGebruikerException):
        service.maak_relatie(gebruiker_id, taak_id)

def test_maak_relatie_invalid_taak(service):
    gebruiker_id = 1
    taak_id = None
    with pytest.raises(InvalidVernietigingstaakException):
        service.maak_relatie(gebruiker_id, taak_id)

def test_bestaat_relatie_true(service):
    gebruiker_id = 2
    taak_id = 3
    with patch("src.services.vtarchivarisrelatie.VTArchivarisRelatieOpslag") as MockOpslag:
        opslag_mock = MagicMock()
        MockOpslag.return_value = opslag_mock
        opslag_mock.bestaat_relatie.return_value = True
        service.ops = opslag_mock
        assert service.bestaat_relatie(gebruiker_id, taak_id)

def test_bestaat_relatie_false(service):
    gebruiker_id = 2
    taak_id = 3
    with patch("src.services.vtarchivarisrelatie.VTArchivarisRelatieOpslag") as MockOpslag:
        opslag_mock = MagicMock()
        MockOpslag.return_value = opslag_mock
        opslag_mock.bestaat_relatie.return_value = False
        service.ops = opslag_mock
        assert service.bestaat_relatie(gebruiker_id, taak_id) is False