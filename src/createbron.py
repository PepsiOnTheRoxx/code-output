class BronCreationException(Exception):
    pass

class Bron:
    def __init__(self, naam, beschrijving):
        self.naam = naam
        self.beschrijving = beschrijving

class BronService:
    def create_bron(self, naam, beschrijving):
        if not naam or not beschrijving:
            raise BronCreationException("Naam en beschrijving zijn vereist.")
        return Bron(naam, beschrijving)

def main():
    service = BronService()
    try:
        bron = service.create_bron("Voorbeeld Bron", "Dit is een beschrijving van de bron.")
        print(f"Bron gecreëerd: {bron.naam} - {bron.beschrijving}")
    except BronCreationException as e:
        print(f"Fout bij het creëren van bron: {e}")

if __name__ == "__main__":
    main()