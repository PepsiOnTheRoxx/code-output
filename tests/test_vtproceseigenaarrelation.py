import pytest
from src.vtproceseigenaarrelation import DestructionTaskService, Gebruiker, Vernietigingstaak, ProceseigenaarAlreadyExists, ProceseigenaarNotFound, InvalidGebruikerOrVernietigingstaak

@pytest.fixture
def service():
    return DestructionTaskService()

@pytest.fixture
def gebruiker():
    return Gebruiker(id=1, naam="testuser")

@pytest.fixture
def vernietigingstaak():
    return Vernietigingstaak(id=100, omschrijving="Verwijder archiefstuk")

def test_add_proceseigenaar_relation_success(service, gebruiker, vernietigingstaak):
    service.add_proceseigenaar(gebruiker, vernietigingstaak)
    assert service.is_proceseigenaar(gebruiker, vernietigingstaak) is True

def test_add_proceseigenaar_relation_duplicate_raises(service, gebruiker, vernietigingstaak):
    service.add_proceseigenaar(gebruiker, vernietigingstaak)
    with pytest.raises(ProceseigenaarAlreadyExists):
        service.add_proceseigenaar(gebruiker, vernietigingstaak)

def test_remove_proceseigenaar_relation_success(service, gebruiker, vernietigingstaak):
    service.add_proceseigenaar(gebruiker, vernietigingstaak)
    service.remove_proceseigenaar(gebruiker, vernietigingstaak)
    assert service.is_proceseigenaar(gebruiker, vernietigingstaak) is False

def test_remove_proceseigenaar_relation_not_found_raises(service, gebruiker, vernietigingstaak):
    with pytest.raises(ProceseigenaarNotFound):
        service.remove_proceseigenaar(gebruiker, vernietigingstaak)

def test_is_proceseigenaar_returns_false_when_not_set(service, gebruiker, vernietigingstaak):
    assert service.is_proceseigenaar(gebruiker, vernietigingstaak) is False

def test_add_proceseigenaar_invalid_arguments_raises(service):
    with pytest.raises(InvalidGebruikerOrVernietigingstaak):
        service.add_proceseigenaar(None, None)

def test_multiple_proceseigenaren_for_different_taak(service, gebruiker):
    vernietigingstaak1 = Vernietigingstaak(id=101, omschrijving="Vernietig documenten 1")
    vernietigingstaak2 = Vernietigingstaak(id=102, omschrijving="Vernietig documenten 2")
    service.add_proceseigenaar(gebruiker, vernietigingstaak1)
    service.add_proceseigenaar(gebruiker, vernietigingstaak2)
    assert service.is_proceseigenaar(gebruiker, vernietigingstaak1) is True
    assert service.is_proceseigenaar(gebruiker, vernietigingstaak2) is True

def test_proceseigenaar_relations_are_isolated(service, gebruiker):
    gebruiker2 = Gebruiker(id=2, naam="anderepersoon")
    vernietigingstaak = Vernietigingstaak(id=103, omschrijving="Opschonen archief")
    service.add_proceseigenaar(gebruiker, vernietigingstaak)
    assert service.is_proceseigenaar(gebruiker, vernietigingstaak) is True
    assert service.is_proceseigenaar(gebruiker2, vernietigingstaak) is False

def test_add_and_remove_multiple_relations(service):
    gebruiker1 = Gebruiker(id=3, naam="g1")
    gebruiker2 = Gebruiker(id=4, naam="g2")
    taak1 = Vernietigingstaak(id=200, omschrijving="Task 1")
    taak2 = Vernietigingstaak(id=201, omschrijving="Task 2")
    service.add_proceseigenaar(gebruiker1, taak1)
    service.add_proceseigenaar(gebruiker2, taak2)
    service.remove_proceseigenaar(gebruiker1, taak1)
    assert service.is_proceseigenaar(gebruiker1, taak1) is False
    assert service.is_proceseigenaar(gebruiker2, taak2) is True