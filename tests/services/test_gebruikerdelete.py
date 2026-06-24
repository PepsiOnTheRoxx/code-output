import pytest
from src.services.gebruikerdelete import GebruikerService
from src.services.gebruikerdelete_exceptions import GebruikerBestaatNietException, VerwijderNietToegestaanException

@pytest.fixture
def gebruiker_service(mocker):
    service = GebruikerService()
    return service

def test_verwijder_bestaande_gebruiker(mocker, gebruiker_service):
    mock_verwijder = mocker.patch.object(gebruiker_service, '_verwijder_gebruiker', return_value=True)
    gebruiker_id = 42
    resultaat = gebruiker_service.verwijder(gebruiker_id)
    assert resultaat is True
    mock_verwijder.assert_called_once_with(gebruiker_id)

def test_verwijder_gebruiker_niet_bestaat(mocker, gebruiker_service):
    gebruiker_id = 100
    mocker.patch.object(gebruiker_service, '_verwijder_gebruiker', side_effect=GebruikerBestaatNietException)
    with pytest.raises(GebruikerBestaatNietException):
        gebruiker_service.verwijder(gebruiker_id)

def test_verwijder_gebruiker_niet_toegestaan(mocker, gebruiker_service):
    gebruiker_id = 23
    mocker.patch.object(gebruiker_service, '_verwijder_gebruiker', side_effect=VerwijderNietToegestaanException)
    with pytest.raises(VerwijderNietToegestaanException):
        gebruiker_service.verwijder(gebruiker_id)

def test_verwijder_gebruiker_geen_side_effect_bij_fout(mocker, gebruiker_service):
    gebruiker_id = 77
    mocker.patch.object(gebruiker_service, '_verwijder_gebruiker', side_effect=GebruikerBestaatNietException)
    with pytest.raises(GebruikerBestaatNietException):
        gebruiker_service.verwijder(gebruiker_id)
    # Optioneel: check geen extra acties or logica na exception

def test_verwijder_gebruiker_met_meerdere_calls(mocker, gebruiker_service):
    gebruiker_id_1 = 10
    gebruiker_id_2 = 20
    mocker.patch.object(gebruiker_service, '_verwijder_gebruiker', side_effect=[True, GebruikerBestaatNietException()])
    resultaat = gebruiker_service.verwijder(gebruiker_id_1)
    assert resultaat is True
    with pytest.raises(GebruikerBestaatNietException):
        gebruiker_service.verwijder(gebruiker_id_2)