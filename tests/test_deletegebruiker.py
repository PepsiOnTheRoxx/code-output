import pytest
from src.deletegebruiker import GebruikerService
from src.deletegebruiker_exceptions import GebruikerNotFound, UnauthorizedOperation, GebruikerDeleteError

@pytest.fixture
def gebruiker_service(mocker):
    return GebruikerService()

def test_verwijder_gebruiker_succes(gebruiker_service, mocker):
    gebruiker_id = 42
    mocker.patch.object(gebruiker_service, "bestaat_gebruiker", return_value=True)
    mocker.patch.object(gebruiker_service, "mag_verwijderen", return_value=True)
    mocker.patch.object(gebruiker_service, "verwijder_gebruiker_uit_db", return_value=None)

    gebruiker_service.verwijder_gebruiker(gebruiker_id)

def test_verwijder_gebruiker_niet_gevonden(gebruiker_service, mocker):
    gebruiker_id = 43
    mocker.patch.object(gebruiker_service, "bestaat_gebruiker", return_value=False)

    with pytest.raises(GebruikerNotFound):
        gebruiker_service.verwijder_gebruiker(gebruiker_id)

def test_verwijder_gebruiker_ongeautoriseerd(gebruiker_service, mocker):
    gebruiker_id = 44
    mocker.patch.object(gebruiker_service, "bestaat_gebruiker", return_value=True)
    mocker.patch.object(gebruiker_service, "mag_verwijderen", return_value=False)

    with pytest.raises(UnauthorizedOperation):
        gebruiker_service.verwijder_gebruiker(gebruiker_id)

def test_verwijder_gebruiker_db_fout(gebruiker_service, mocker):
    gebruiker_id = 45
    mocker.patch.object(gebruiker_service, "bestaat_gebruiker", return_value=True)
    mocker.patch.object(gebruiker_service, "mag_verwijderen", return_value=True)
    mocker.patch.object(gebruiker_service, "verwijder_gebruiker_uit_db", side_effect=GebruikerDeleteError)

    with pytest.raises(GebruikerDeleteError):
        gebruiker_service.verwijder_gebruiker(gebruiker_id)