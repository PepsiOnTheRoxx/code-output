class Gebruiker:
    def __init__(self, naam, email):
        self.naam = naam
        self.email = email

class UserService:
    def __init__(self):
        self.gebruikers = []

    def create_gebruiker(self, naam, email):
        if not naam or not email:
            raise ValueError("Naam en email mogen niet leeg zijn.")
        if any(g.email == email for g in self.gebruikers):
            raise ValueError("Email is al in gebruik.")
        nieuwe_gebruiker = Gebruiker(naam, email)
        self.gebruikers.append(nieuwe_gebruiker)
        return nieuwe_gebruiker

def test_create_gebruiker_met_geldige_data():
    service = UserService()
    gebruiker = service.create_gebruiker("Jan Jansen", "jan@example.com")
    assert gebruiker.naam == "Jan Jansen"
    assert gebruiker.email == "jan@example.com"
    assert len(service.gebruikers) == 1

def test_create_gebruiker_met_lege_naam():
    service = UserService()
    with pytest.raises(ValueError, match="Naam en email mogen niet leeg zijn."):
        service.create_gebruiker("", "jan@example.com")

def test_create_gebruiker_met_leeg_email():
    service = UserService()
    with pytest.raises(ValueError, match="Naam en email mogen niet leeg zijn."):
        service.create_gebruiker("Jan Jansen", "")

def test_create_gebruiker_met_dubbel_email():
    service = UserService()
    service.create_gebruiker("Jan Jansen", "jan@example.com")
    with pytest.raises(ValueError, match="Email is al in gebruik."):
        service.create_gebruiker("Piet Pietersen", "jan@example.com")

def test_create_gebruiker_verhoogt_gebruikers_count():
    service = UserService()
    service.create_gebruiker("Jan Jansen", "jan@example.com")
    service.create_gebruiker("Piet Pietersen", "piet@example.com")
    assert len(service.gebruikers) == 2

# To run the tests:
if __name__ == "__main__":
    test_create_gebruiker_met_geldige_data()
    test_create_gebruiker_met_lege_naam()
    test_create_gebruiker_met_leeg_email()
    test_create_gebruiker_met_dubbel_email()
    test_create_gebruiker_verhoogt_gebruikers_count()