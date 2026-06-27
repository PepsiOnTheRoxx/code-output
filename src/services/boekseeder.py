from src.services.boekseeder_exceptions import (
    BoekSeederException,
    BoekSeederToevoegenMisluktException
)

class BoekSeeder:
    def __init__(self, boek_service):
        self.boek_service = boek_service

    def seed(self):
        boeken = [
            {
                'auteur': "Arthur Conan Doyle",
                'beschrijving': "Een klassiek mysterieboek met detective Sherlock Holmes.",
                'titel': "Sherlock Holmes Verhalenbundel",  # Toegevoegd
                'isbn': "9789012345678",
                'publicatiedatum': "1892-10-14",
                'kaft_foto_url': "http://dummy.url/holmes.jpg",
                'is_uitgeleend': False,
                'uitgeleend_datum': None,
                'uitgeleend_max_tot': None
            },
            {
                'auteur': "J.K. Rowling",
                'beschrijving': "Het eerste deel in de magische Harry Potter-serie.",
                'titel': "Harry Potter en de Steen der Wijzen",  # Toegevoegd
                'isbn': "9780747532743",
                'publicatiedatum': "1997-06-26",
                'kaft_foto_url': "http://dummy.url/hp1.jpg",
                'is_uitgeleend': True,
                'uitgeleend_datum': "2023-07-10",
                'uitgeleend_max_tot': "2023-08-10"
            },
            {
                'auteur': "George Orwell",
                'beschrijving': "Dystopische roman over een totalitaire samenleving.",
                'titel': "1984",  # Toegevoegd
                'isbn': "9780451524935",
                'publicatiedatum': "1949-06-08",
                'kaft_foto_url': "http://dummy.url/1984.jpg",
                'is_uitgeleend': False,
                'uitgeleend_datum': None,
                'uitgeleend_max_tot': None
            },
            {
                'auteur': "Harper Lee",
                'beschrijving': "Een diepgaand verhaal over racisme en onschuld.",
                'titel': "To Kill a Mockingbird",  # Toegevoegd
                'isbn': "9780061120084",
                'publicatiedatum': "1960-07-11",
                'kaft_foto_url': "http://dummy.url/mockingbird.jpg",
                'is_uitgeleend': True,
                'uitgeleend_datum': "2024-01-01",
                'uitgeleend_max_tot': "2024-01-31"
            },
            {
                'auteur': "F. Scott Fitzgerald",
                'beschrijving': "Amerikaans meesterwerk over The Jazz Age.",
                'titel': "The Great Gatsby",  # Toegevoegd
                'isbn': "9780743273565",
                'publicatiedatum': "1925-04-10",
                'kaft_foto_url': "http://dummy.url/gatsby.jpg",
                'is_uitgeleend': False,
                'uitgeleend_datum': None,
                'uitgeleend_max_tot': None
            }
        ]
        try:
            for boek in boeken:
                self.boek_service.voeg_toe(boek)
        except Exception as e:
            raise BoekSeederToevoegenMisluktException(str(e))
