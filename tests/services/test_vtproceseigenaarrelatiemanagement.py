import pytest
from src.services.vtproceseigenaarrelatiemanagement import VTProceseigenaarRelatieService
from src.services.vtproceseigenaarrelatiemanagement_exceptions import RelatieBestaatAlException, RelatieNietGevondenException

@pytest.fixture
def service():
    return VTProceseigenaarRelatieService()

def test_koppel_gebruiker_als_proceseigenaar(service):
    vernietigingstaak_id = 1
    gebruiker_id = 10
    service.koppel_proceseigenaar(vernietigingstaak_id, gebruiker_id)
    gekoppeld = service.is_proceseigenaar(vernietigingstaak_id, gebruiker_id)
    assert gekoppeld is True

def test_koppel_gebruiker_als_proceseigenaar_bestaat_al(service):
    vernietigingstaak_id = 2
    gebruiker_id = 20
    service.koppel_proceseigenaar(vernietigingstaak_id, gebruiker_id)
    with pytest.raises(RelatieBestaatAlException):
        service.koppel_proceseigenaar(vernietigingstaak_id, gebruiker_id)

def test_verwijder_proceseigenaar_relatie(service):
    vernietigingstaak_id = 3
    gebruiker_id = 30
    service.koppel_proceseigenaar(vernietigingstaak_id, gebruiker_id)
    service.verwijder_proceseigenaar_relatie(vernietigingstaak_id, gebruiker_id)
    gekoppeld = service.is_proceseigenaar(vernietigingstaak_id, gebruiker_id)
    assert gekoppeld is False

def test_verwijder_proceseigenaar_relatie_bestaat_niet(service):
    vernietigingstaak_id = 4
    gebruiker_id = 40
    with pytest.raises(RelatieNietGevondenException):
        service.verwijder_proceseigenaar_relatie(vernietigingstaak_id, gebruiker_id)

def test_is_proceseigenaar_false(service):
    vernietigingstaak_id = 5
    gebruiker_id = 50
    gekoppeld = service.is_proceseigenaar(vernietigingstaak_id, gebruiker_id)
    assert gekoppeld is False

def test_meerdere_proceseigenaars_op_een_vernietigingstaak(service):
    vernietigingstaak_id = 6
    gebruiker_id_1 = 60
    gebruiker_id_2 = 61
    service.koppel_proceseigenaar(vernietigingstaak_id, gebruiker_id_1)
    service.koppel_proceseigenaar(vernietigingstaak_id, gebruiker_id_2)
    assert service.is_proceseigenaar(vernietigingstaak_id, gebruiker_id_1) is True
    assert service.is_proceseigenaar(vernietigingstaak_id, gebruiker_id_2) is True

def test_lijst_proceseigenaars_op_vernietigingstaak(service):
    vernietigingstaak_id = 7
    gebruikers = [70, 71, 72]
    for gebruiker_id in gebruikers:
        service.koppel_proceseigenaar(vernietigingstaak_id, gebruiker_id)
    proceseigenaars = service.lijst_proceseigenaars(vernietigingstaak_id)
    assert set(proceseigenaars) == set(gebruikers)

def test_lijst_proceseigenaars_op_vernietigingstaak_geen(service):
    vernietigingstaak_id = 8
    proceseigenaars = service.lijst_proceseigenaars(vernietigingstaak_id)
    assert proceseigenaars == []