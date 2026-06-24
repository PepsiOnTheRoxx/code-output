import pytest

class Gebruiker:
    def __init__(self, gebruikersnaam, email):
        if not gebruikersnaam or not email:
            raise ValueError("Gebruikersnaam en email zijn verplicht.")
        self.gebruikersnaam = gebruikersnaam
        self.email = email

class UserService:
    def __init__(self):
        self.gebruikers = []

    def create_gebruiker(self, gebruikersnaam, email):
        gebruiker = Gebruiker(gebruikersnaam, email)
        self.gebruikers.append(gebruiker)
        return gebruiker

    def get_gebruikers(self):
        return self.gebruikers

def test_create_gebruiker_success():
    user_service = UserService()
    gebruiker = user_service.create_gebruiker("testuser", "test@example.com")
    
    assert gebruiker.gebruikersnaam == "testuser"
    assert gebruiker.email == "test@example.com"
    assert len(user_service.get_gebruikers()) == 1

def test_create_gebruiker_missing_gebruikersnaam():
    user_service = UserService()
    
    with pytest.raises(ValueError, match="Gebruikersnaam en email zijn verplicht."):
        user_service.create_gebruiker("", "test@example.com")

def test_create_gebruiker_missing_email():
    user_service = UserService()
    
    with pytest.raises(ValueError, match="Gebruikersnaam en email zijn verplicht."):
        user_service.create_gebruiker("testuser", "")

def test_create_gebruiker_multiple_instances():
    user_service = UserService()
    gebruiker1 = user_service.create_gebruiker("user1", "user1@example.com")
    gebruiker2 = user_service.create_gebruiker("user2", "user2@example.com")
    
    assert len(user_service.get_gebruikers()) == 2
    assert gebruiker1.gebruikersnaam == "user1"
    assert gebruiker2.gebruikersnaam == "user2"

def test_create_gebruiker_unique_data():
    user_service = UserService()
    gebruiker1 = user_service.create_gebruiker("uniqueuser", "unique@example.com")
    
    assert gebruiker1.gebruikersnaam != "anotheruser"  
    assert gebruiker1.email != "another@example.com"