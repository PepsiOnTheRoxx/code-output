import pytest

class Vernietigingstaak:
    def __init__(self, aantekeningen, datum, status):
        self.aantekeningen = aantekeningen
        self.datum = datum
        self.status = status

class VernietigingstaakService:
    def create_vernietigingstaak(self, aantekeningen, datum, status):
        if not aantekeningen or not datum or not status:
            raise ValueError("Alle velden moeten ingevuld zijn.")
        return Vernietigingstaak(aantekeningen, datum, status)

def test_create_vernietigingstaak_success():
    service = VernietigingstaakService()
    taak = service.create_vernietigingstaak("Test aantekeningen", "2023-10-01", "Nieuw")
    assert taak.aantekeningen == "Test aantekeningen"
    assert taak.datum == "2023-10-01"
    assert taak.status == "Nieuw"

def test_create_vernietigingstaak_empty_aantekeningen():
    service = VernietigingstaakService()
    with pytest.raises(ValueError, match="Alle velden moeten ingevuld zijn."):
        service.create_vernietigingstaak("", "2023-10-01", "Nieuw")

def test_create_vernietigingstaak_empty_datum():
    service = VernietigingstaakService()
    with pytest.raises(ValueError, match="Alle velden moeten ingevuld zijn."):
        service.create_vernietigingstaak("Test aantekeningen", "", "Nieuw")

def test_create_vernietigingstaak_empty_status():
    service = VernietigingstaakService()
    with pytest.raises(ValueError, match="Alle velden moeten ingevuld zijn."):
        service.create_vernietigingstaak("Test aantekeningen", "2023-10-01", "")

def test_create_vernietigingstaak_all_empty():
    service = VernietigingstaakService()
    with pytest.raises(ValueError, match="Alle velden moeten ingevuld zijn."):
        service.create_vernietigingstaak("", "", "")