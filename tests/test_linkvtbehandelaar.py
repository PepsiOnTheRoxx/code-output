import pytest
from src.linkvtbehandelaar import VernietigingstaakRelatiesService
from src.linkvtbehandelaar_exceptions import (
    LinkVTBehandelaarGebruikerNotFound,
    LinkVTBehandelaarVernietigingstaakNotFound,
    LinkVTBehandelaarAlreadyLinked,
)

def test_link_gebruiker_als_behandelaar_succesvol(monkeypatch):
    service = VernietigingstaakRelatiesService()
    gebruiker_id = 10
    vernietigingstaak_id = 20

    monkeypatch.setattr(service, "gebruiker_bestaat", lambda x: True)
    monkeypatch.setattr(service, "vernietigingstaak_bestaat", lambda x: True)
    monkeypatch.setattr(service, "is_behandelaar", lambda x, y: False)
    called = {}
    def fake_link(gebruiker_id_, vernietigingstaak_id_):
        called['called'] = (gebruiker_id_, vernietigingstaak_id_)
    monkeypatch.setattr(service, "link_behandelaar_aan_taak", fake_link)

    service.link_gebruiker_als_behandelaar(gebruiker_id, vernietigingstaak_id)

    assert called['called'] == (gebruiker_id, vernietigingstaak_id)

def test_link_gebruiker_als_behandelaar_gebruiker_niet_gevonden(monkeypatch):
    service = VernietigingstaakRelatiesService()
    gebruiker_id = 11
    vernietigingstaak_id = 21

    monkeypatch.setattr(service, "gebruiker_bestaat", lambda x: False)

    with pytest.raises(LinkVTBehandelaarGebruikerNotFound):
        service.link_gebruiker_als_behandelaar(gebruiker_id, vernietigingstaak_id)

def test_link_gebruiker_als_behandelaar_taak_niet_gevonden(monkeypatch):
    service = VernietigingstaakRelatiesService()
    gebruiker_id = 12
    vernietigingstaak_id = 22

    monkeypatch.setattr(service, "gebruiker_bestaat", lambda x: True)
    monkeypatch.setattr(service, "vernietigingstaak_bestaat", lambda x: False)

    with pytest.raises(LinkVTBehandelaarVernietigingstaakNotFound):
        service.link_gebruiker_als_behandelaar(gebruiker_id, vernietigingstaak_id)

def test_link_gebruiker_als_behandelaar_al_gekoppeld(monkeypatch):
    service = VernietigingstaakRelatiesService()
    gebruiker_id = 13
    vernietigingstaak_id = 23

    monkeypatch.setattr(service, "gebruiker_bestaat", lambda x: True)
    monkeypatch.setattr(service, "vernietigingstaak_bestaat", lambda x: True)
    monkeypatch.setattr(service, "is_behandelaar", lambda x, y: True)

    with pytest.raises(LinkVTBehandelaarAlreadyLinked):
        service.link_gebruiker_als_behandelaar(gebruiker_id, vernietigingstaak_id)
