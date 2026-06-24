import pytest
from unittest.mock import patch, MagicMock
from src.services.vtbehandelaarrelatie import VTBehandelaarRelatieService
from src.services.vtbehandelaarrelatie_exceptions import (
    VTBehandelaarRelatieBestaatAlException,
    VTBehandelaarRelatieNietGevondenException,
    OngeldigeGebruikerException,
    OngeldigeVernietigingstaakException,
)

def test_maak_relatie_succesvol():
    service = VTBehandelaarRelatieService()
    gebruiker_id = 10
    taak_id = 20

    with patch.object(service, 'controleer_of_gebruiker_bestaat', return_value=True) as mock_gebruiker, \
         patch.object(service, 'controleer_of_taak_bestaat', return_value=True) as mock_taak, \
         patch.object(service, 'bestaat_relatie', return_value=False) as mock_bestaat, \
         patch.object(service, 'opslaan_relatie', return_value=None) as mock_opslaan:
        service.maak_relatie(gebruiker_id, taak_id)
        mock_gebruiker.assert_called_once_with(gebruiker_id)
        mock_taak.assert_called_once_with(taak_id)
        mock_bestaat.assert_called_once_with(gebruiker_id, taak_id)
        mock_opslaan.assert_called_once_with(gebruiker_id, taak_id)

def test_maak_relatie_bestaat_al():
    service = VTBehandelaarRelatieService()
    gebruiker_id = 11
    taak_id = 21

    with patch.object(service, 'controleer_of_gebruiker_bestaat', return_value=True), \
         patch.object(service, 'controleer_of_taak_bestaat', return_value=True), \
         patch.object(service, 'bestaat_relatie', return_value=True):
        with pytest.raises(VTBehandelaarRelatieBestaatAlException):
            service.maak_relatie(gebruiker_id, taak_id)

def test_maak_relatie_ongeldige_gebruiker():
    service = VTBehandelaarRelatieService()
    gebruiker_id = 12
    taak_id = 22

    with patch.object(service, 'controleer_of_gebruiker_bestaat', return_value=False):
        with pytest.raises(OngeldigeGebruikerException):
            service.maak_relatie(gebruiker_id, taak_id)

def test_maak_relatie_ongeldige_taak():
    service = VTBehandelaarRelatieService()
    gebruiker_id = 15
    taak_id = 25

    with patch.object(service, 'controleer_of_gebruiker_bestaat', return_value=True), \
         patch.object(service, 'controleer_of_taak_bestaat', return_value=False):
        with pytest.raises(OngeldigeVernietigingstaakException):
            service.maak_relatie(gebruiker_id, taak_id)

def test_verwijder_relatie_succesvol():
    service = VTBehandelaarRelatieService()
    gebruiker_id = 30
    taak_id = 40

    with patch.object(service, 'bestaat_relatie', return_value=True) as mock_bestaat, \
         patch.object(service, 'verwijder_relatie', return_value=None) as mock_verwijder:
        service.verwijder_relatie(gebruiker_id, taak_id)
        mock_bestaat.assert_called_once_with(gebruiker_id, taak_id)
        mock_verwijder.assert_called_once_with(gebruiker_id, taak_id)

def test_verwijder_relatie_niet_gevonden():
    service = VTBehandelaarRelatieService()
    gebruiker_id = 31
    taak_id = 41

    with patch.object(service, 'bestaat_relatie', return_value=False):
        with pytest.raises(VTBehandelaarRelatieNietGevondenException):
            service.verwijder_relatie(gebruiker_id, taak_id)

def test_haal_relaties_op_succesvol():
    service = VTBehandelaarRelatieService()
    gebruiker_id = 50
    mock_result = [
        {'gebruiker_id': gebruiker_id, 'taak_id': 60},
        {'gebruiker_id': gebruiker_id, 'taak_id': 61},
    ]

    with patch.object(service, 'haal_relaties_op_voor_gebruiker', return_value=mock_result) as mock_haal:
        relaties = service.haal_relaties_op(gebruiker_id)
        mock_haal.assert_called_once_with(gebruiker_id)
        assert relaties == mock_result

def test_haal_relaties_op_ongeldige_gebruiker():
    service = VTBehandelaarRelatieService()
    gebruiker_id = 70

    with patch.object(service, 'controleer_of_gebruiker_bestaat', return_value=False):
        with pytest.raises(OngeldigeGebruikerException):
            service.haal_relaties_op(gebruiker_id)