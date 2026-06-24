import pytest
from src.updategebruiker import UserService, GebruikerNotFoundException, InvalidGebruikerDataException

@pytest.fixture
def user_service():
    service = UserService()
    service._gebruikers = {
        1: {'id': 1, 'naam': 'Jan', 'email': 'jan@example.com'},
        2: {'id': 2, 'naam': 'Piet', 'email': 'piet@example.com'},
    }
    return service

def test_update_existing_gebruiker_success(user_service):
    updated_data = {'naam': 'Jan Jansen', 'email': 'jan.jansen@example.com'}
    gebruiker = user_service.update_gebruiker(1, updated_data)
    assert gebruiker['id'] == 1
    assert gebruiker['naam'] == 'Jan Jansen'
    assert gebruiker['email'] == 'jan.jansen@example.com'
    assert user_service._gebruikers[1]['naam'] == 'Jan Jansen'
    assert user_service._gebruikers[1]['email'] == 'jan.jansen@example.com'

def test_update_non_existing_gebruiker_raises(user_service):
    updated_data = {'naam': 'Klaas', 'email': 'klaas@example.com'}
    with pytest.raises(GebruikerNotFoundException):
        user_service.update_gebruiker(99, updated_data)

def test_update_partial_data_name_only(user_service):
    updated_data = {'naam': 'Jan Updated'}
    gebruiker = user_service.update_gebruiker(1, updated_data)
    assert gebruiker['naam'] == 'Jan Updated'
    assert gebruiker['email'] == 'jan@example.com'
    assert user_service._gebruikers[1]['naam'] == 'Jan Updated'

def test_update_partial_data_email_only(user_service):
    updated_data = {'email': 'jan.new@example.com'}
    gebruiker = user_service.update_gebruiker(1, updated_data)
    assert gebruiker['naam'] == 'Jan'
    assert gebruiker['email'] == 'jan.new@example.com'
    assert user_service._gebruikers[1]['email'] == 'jan.new@example.com'

def test_update_with_invalid_id_type_raises(user_service):
    updated_data = {'naam': 'Jan StringId', 'email': 'jan.stringid@example.com'}
    with pytest.raises(GebruikerNotFoundException):
        user_service.update_gebruiker('one', updated_data)

def test_update_with_none_as_data_raises(user_service):
    with pytest.raises(InvalidGebruikerDataException):
        user_service.update_gebruiker(1, None)

def test_update_with_empty_data_does_not_change_gebruiker(user_service):
    existing_user = user_service._gebruikers[1].copy()
    gebruiker = user_service.update_gebruiker(1, {})
    assert gebruiker == existing_user
    assert user_service._gebruikers[1] == existing_user

def test_update_with_extra_unknown_fields_ignores_them(user_service):
    updated_data = {'naam': 'Jan', 'email': 'jan@example.com', 'onbekend': 'waarde'}
    gebruiker = user_service.update_gebruiker(1, updated_data)
    assert gebruiker['naam'] == 'Jan'
    assert gebruiker['email'] == 'jan@example.com'
    assert 'onbekend' not in gebruiker
    assert 'onbekend' not in user_service._gebruikers[1]