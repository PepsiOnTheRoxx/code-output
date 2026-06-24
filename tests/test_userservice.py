import pytest
from src.userservice import UserService, Gebruiker

class TestUserService:
    @pytest.fixture
    def user_service(self):
        return UserService()

    def test_create_gebruiker_success(self, user_service):
        gebruiker_data = {
            'gebruikersnaam': 'testuser',
            'email': 'testuser@example.com',
            'wachtwoord': 'securepassword'
        }
        gebruiker = user_service.create_gebruiker(gebruiker_data)
        assert isinstance(gebruiker, Gebruiker)
        assert gebruiker.gebruikersnaam == 'testuser'
        assert gebruiker.email == 'testuser@example.com'
        assert gebruiker.wachtwoord != 'securepassword'

    def test_create_gebruiker_missing_data(self, user_service):
        gebruiker_data = {
            'gebruikersnaam': 'testuser'
        }
        with pytest.raises(ValueError) as exc_info:
            user_service.create_gebruiker(gebruiker_data)
        assert str(exc_info.value) == 'Missing required gebruiker information'

    def test_create_gebruiker_invalid_email(self, user_service):
        gebruiker_data = {
            'gebruikersnaam': 'testuser',
            'email': 'invalid_email',
            'wachtwoord': 'securepassword'
        }
        with pytest.raises(ValueError) as exc_info:
            user_service.create_gebruiker(gebruiker_data)
        assert str(exc_info.value) == 'Invalid email format'

    def test_create_gebruiker_duplicate(self, user_service):
        gebruiker_data = {
            'gebruikersnaam': 'testuser',
            'email': 'testuser@example.com',
            'wachtwoord': 'securepassword'
        }
        user_service.create_gebruiker(gebruiker_data)
        with pytest.raises(ValueError) as exc_info:
            user_service.create_gebruiker(gebruiker_data)
        assert str(exc_info.value) == 'Gebruiker already exists'