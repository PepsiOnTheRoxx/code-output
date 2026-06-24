import pytest
from datetime import date
from src.createvernietigingstaak import VernietigingstaakService
from src.createvernietigingstaak_exceptions import (
    InvalidStatusException,
    MissingAantekeningenException,
    MissingDatumException,
)

def test_create_vernietigingstaak_succesvolle_aanmaak():
    service = VernietigingstaakService()
    taak = service.create_vernietigingstaak(
        aantekeningen="Aantekeningen over de vernietiging",
        datum=date(2024, 6, 15),
        status="InBehandeling"
    )
    assert taak.aantekeningen == "Aantekeningen over de vernietiging"
    assert taak.datum == date(2024, 6, 15)
    assert taak.status == "InBehandeling"

def test_create_vernietigingstaak_leeg_aantekeningen():
    service = VernietigingstaakService()
    with pytest.raises(MissingAantekeningenException):
        service.create_vernietigingstaak(
            aantekeningen="",
            datum=date(2024, 6, 15),
            status="InBehandeling"
        )

def test_create_vernietigingstaak_zonder_datum():
    service = VernietigingstaakService()
    with pytest.raises(MissingDatumException):
        service.create_vernietigingstaak(
            aantekeningen="Test aantekening",
            datum=None,
            status="InBehandeling"
        )

def test_create_vernietigingstaak_onbekende_status():
    service = VernietigingstaakService()
    with pytest.raises(InvalidStatusException):
        service.create_vernietigingstaak(
            aantekeningen="Test aantekening",
            datum=date(2024, 6, 15),
            status="NietBestaandeStatus"
        )

def test_create_vernietigingstaak_status_afgerond():
    service = VernietigingstaakService()
    taak = service.create_vernietigingstaak(
        aantekeningen="Vernietiging uitgevoerd",
        datum=date(2024, 6, 16),
        status="Afgerond"
    )
    assert taak.status == "Afgerond"
    assert taak.aantekeningen == "Vernietiging uitgevoerd"
    assert taak.datum == date(2024, 6, 16)