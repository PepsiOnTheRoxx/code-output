import pytest
from src.linkvtbehandelaar import VernietigingstaakRelatiesService
from src.linkvtbehandelaar_exceptions import (
    GebruikerNietGevondenException,
    VernietigingstaakNietGevondenException,
    BehandelaarAlGekoppeldException,
)


def test_link_gebruiker_als_behandelaar_succesvol(mocker):
    service = VernietigingstaakRelatiesService()
    gebruiker_id = 10
    vernietigingstaak_id = 20

    mocker.patch.object(service, "gebruiker_bestaat", return_value=True)
    mocker.patch.object(service, "vernietigingstaak_bestaat", return_value=True)
    mocker.patch.object(service, "is_behandelaar", return_value=False)
    mock_link = mocker.patch.object(service, "link_behandelaar_aan_taak")

    service.link_gebruiker_als_behandelaar(gebruiker_id, vernietigingstaak_id)

    mock_link.assert_called_once_with(gebruiker_id, vernietigingstaak_id)


def test_link_gebruiker_als_behandelaar_gebruiker_niet_gevonden(mocker):
    service = VernietigingstaakRelatiesService()
    gebruiker_id = 11
    vernietigingstaak_id = 21

    mocker.patch.object(service, "gebruiker_bestaat", return_value=False)

    with pytest.raises(GebruikerNietGevondenException):
        service.link_gebruiker_als_behandelaar(gebruiker_id, vernietigingstaak_id)


def test_link_gebruiker_als_behandelaar_taak_niet_gevonden(mocker):
    service = VernietigingstaakRelatiesService()
    gebruiker_id = 12
    vernietigingstaak_id = 22

    mocker.patch.object(service, "gebruiker_bestaat", return_value=True)
    mocker.patch.object(service, "vernietigingstaak_bestaat", return_value=False)

    with pytest.raises(VernietigingstaakNietGevondenException):
        service.link_gebruiker_als_behandelaar(gebruiker_id, vernietigingstaak_id)


def test_link_gebruiker_als_behandelaar_al_gekoppeld(mocker):
    service = VernietigingstaakRelatiesService()
    gebruiker_id = 13
    vernietigingstaak_id = 23

    mocker.patch.object(service, "gebruiker_bestaat", return_value=True)
    mocker.patch.object(service, "vernietigingstaak_bestaat", return_value=True)
    mocker.patch.object(service, "is_behandelaar", return_value=True)

    with pytest.raises(BehandelaarAlGekoppeldException):
        service.link_gebruiker_als_behandelaar(gebruiker_id, vernietigingstaak_id)