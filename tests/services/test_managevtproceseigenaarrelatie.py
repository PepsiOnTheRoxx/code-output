import pytest
from unittest.mock import patch, MagicMock
from src.services.managevtproceseigenaarrelatie import VTProceseigenaarRelatieService
from src.services.managevtproceseigenaarrelatie_exceptions import (
    VTProceseigenaarAlBestaandException,
    VTProceseigenaarNietGevondenException,
    VerbodenWijzigingException
)


def test_toevoegen_proceseigenaar_succesvol():
    service = VTProceseigenaarRelatieService()
    gebruiker_id = 42
    vernietigingstaak_id = 7
    with patch.object(service, "bestaat_relatie", return_value=False):
        with patch.object(service, "opslaan_relatie") as mock_opslaan:
            service.toevoegen_proceseigenaar(gebruiker_id, vernietigingstaak_id)
            mock_opslaan.assert_called_once_with(gebruiker_id, vernietigingstaak_id)


def test_toevoegen_proceseigenaar_al_bestaand():
    service = VTProceseigenaarRelatieService()
    gebruiker_id = 11
    vernietigingstaak_id = 3
    with patch.object(service, "bestaat_relatie", return_value=True):
        with pytest.raises(VTProceseigenaarAlBestaandException):
            service.toevoegen_proceseigenaar(gebruiker_id, vernietigingstaak_id)


def test_verwijderen_proceseigenaar_succesvol():
    service = VTProceseigenaarRelatieService()
    gebruiker_id = 54
    vernietigingstaak_id = 20
    with patch.object(service, "bestaat_relatie", return_value=True):
        with patch.object(service, "verwijder_relatie") as mock_verwijder:
            service.verwijderen_proceseigenaar(gebruiker_id, vernietigingstaak_id)
            mock_verwijder.assert_called_once_with(gebruiker_id, vernietigingstaak_id)


def test_verwijderen_proceseigenaar_niet_gevonden():
    service = VTProceseigenaarRelatieService()
    gebruiker_id = 2
    vernietigingstaak_id = 9
    with patch.object(service, "bestaat_relatie", return_value=False):
        with pytest.raises(VTProceseigenaarNietGevondenException):
            service.verwijderen_proceseigenaar(gebruiker_id, vernietigingstaak_id)


def test_gewijzigde_proceseigenaar_verboden():
    service = VTProceseigenaarRelatieService()
    gebruiker_id = 100
    vernietigingstaak_id = 21
    with patch.object(service, "is_wijziging_toegestaan", return_value=False):
        with pytest.raises(VerbodenWijzigingException):
            service.wijzig_proceseigenaar(gebruiker_id, vernietigingstaak_id, nieuwe_gebruiker_id=101)


def test_gewijzigde_proceseigenaar_succesvol():
    service = VTProceseigenaarRelatieService()
    gebruiker_id = 6
    vernietigingstaak_id = 5
    nieuwe_gebruiker_id = 99
    with patch.object(service, "is_wijziging_toegestaan", return_value=True):
        with patch.object(service, "update_relatie") as mock_update:
            service.wijzig_proceseigenaar(gebruiker_id, vernietigingstaak_id, nieuwe_gebruiker_id)
            mock_update.assert_called_once_with(gebruiker_id, vernietigingstaak_id, nieuwe_gebruiker_id)


def test_raadpleeg_proceseigenaar_gevonden():
    service = VTProceseigenaarRelatieService()
    vernietigingstaak_id = 999
    proceseigenaar = {"id": 123, "naam": "Jan"}
    with patch.object(service, "get_proceseigenaar_by_vernietigingstaak", return_value=proceseigenaar):
        result = service.raadpleeg_proceseigenaar(vernietigingstaak_id)
        assert result == proceseigenaar


def test_raadpleeg_proceseigenaar_niet_gevonden():
    service = VTProceseigenaarRelatieService()
    vernietigingstaak_id = 888
    with patch.object(service, "get_proceseigenaar_by_vernietigingstaak", return_value=None):
        with pytest.raises(VTProceseigenaarNietGevondenException):
            service.raadpleeg_proceseigenaar(vernietigingstaak_id)