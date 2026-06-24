class Gebruiker:
    def __init__(self, naam, email):
        if not naam or not email:
            raise ValueError("Naam en email zijn vereist.")
        self.naam = naam
        self.email = email

class UserService:
    def create_gebruiker(self, naam, email):
        return Gebruiker(naam, email)

def test_create_gebruiker_met_geldige_gegevens():
    user_service = UserService()
    gebruiker = user_service.create_gebruiker("Jan Jansen", "jan@example.com")
    assert gebruiker.naam == "Jan Jansen"
    assert gebruiker.email == "jan@example.com"

def test_create_gebruiker_met_leege_naam():
    user_service = UserService()
    with pytest.raises(ValueError, match="Naam en email zijn vereist."):
        user_service.create_gebruiker("", "jan@example.com")

def test_create_gebruiker_met_leeg_email():
    user_service = UserService()
    with pytest.raises(ValueError, match="Naam en email zijn vereist."):
        user_service.create_gebruiker("Jan Jansen", "")

def test_create_gebruiker_met_leeg_naam_en_email():
    user_service = UserService()
    with pytest.raises(ValueError, match="Naam en email zijn vereist."):
        user_service.create_gebruiker("", "")

test_create_gebruiker_met_geldige_gegevens()
test_create_gebruiker_met_leege_naam()
test_create_gebruiker_met_leeg_email()
test_create_gebruiker_met_leeg_naam_en_email()