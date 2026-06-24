import pytest
from datetime import datetime, timedelta
from src.services.vernietigingstaakcreate import VernietigingstaakService
from src.services.vernietigingstaakcreate_exceptions import (
    InvalidDatumException,
    InvalidStatusException,
    MissingAantekeningenException,
)

def test_create_vernietigingstaak_successful():
    service = VernietigingstaakService()
    aantekeningen = "Vernietigen wegens verouderd dossier."
    datum = datetime.today().date()
    status = "AANGEVRAAGD"
    taak = service.create(aantekeningen=aantekeningen, datum=datum, status=status)
    assert taak.aantekeningen == aantekeningen
    assert taak.datum == datum
    assert taak.status == status

def test_create_vernietigingstaak_invalid_datum_in_future():
    service = VernietigingstaakService()
    aantekeningen = "Datum ligt in de toekomst."
    datum = datetime.today().date() + timedelta(days=1)
    status = "AANGEVRAAGD"
    with pytest.raises(InvalidDatumException):
        service.create(aantekeningen=aantekeningen, datum=datum, status=status)

def test_create_vernietigingstaak_missing_aantekeningen():
    service = VernietigingstaakService()
    datum = datetime.today().date()
    status = "AANGEVRAAGD"
    with pytest.raises(MissingAantekeningenException):
        service.create(aantekeningen=None, datum=datum, status=status)

def test_create_vernietigingstaak_invalid_status():
    service = VernietigingstaakService()
    aantekeningen = "Onbekende status test."
    datum = datetime.today().date()
    status = "ONGELDIG"
    with pytest.raises(InvalidStatusException):
        service.create(aantekeningen=aantekeningen, datum=datum, status=status)

def test_create_vernietigingstaak_blank_aantekeningen():
    service = VernietigingstaakService()
    datum = datetime.today().date()
    status = "IN_BEHANDELING"
    with pytest.raises(MissingAantekeningenException):
        service.create(aantekeningen="", datum=datum, status=status)

def test_create_vernietigingstaak_allowed_status_values():
    service = VernietigingstaakService()
    aantekeningen = "Correcte aanmaak met status IN_BEHANDELING."
    datum = datetime.today().date()
    status = "IN_BEHANDELING"
    taak = service.create(aantekeningen=aantekeningen, datum=datum, status=status)
    assert taak.status == status

def test_create_vernietigingstaak_datum_today_is_valid():
    service = VernietigingstaakService()
    aantekeningen = "Datum vandaag is toegestaan."
    datum = datetime.today().date()
    status = "AANGEVRAAGD"
    taak = service.create(aantekeningen=aantekeningen, datum=datum, status=status)
    assert taak.datum == datum
