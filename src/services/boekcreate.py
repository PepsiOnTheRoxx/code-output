from datetime import date
from src.services.boekcreate_exceptions import (
    BoekCreateException,
    BoekCreateDatabaseException,
    BoekCreateMissingAttributeException,
    BoekCreateInvalidAuteurException,
    BoekCreateInvalidBeschrijvingException,
    BoekCreateInvalidIsbnException,
    BoekCreateInvalidPublicatiedatumException,
    BoekCreateInvalidKaftFotoUrlException,
    BoekCreateInvalidIsUitgeleendException,
    BoekCreateInvalidUitgeleendDatumException,
    BoekCreateInvalidUitgeleendMaxTotException,
)

def get_db():
    # Dummy fallback/mock if not patched; in productie overschreven door patch
    raise NotImplementedError("get_db() moet gepatcht worden in tests of worden geimplementeerd.")

class BoekService:
    def __init__(self, db_connection=None):
        if db_connection is None:
            self.db_connection = get_db()
        else:
            self.db_connection = db_connection

    def create_boek(self, **kwargs):
        required_fields = [
            'titel', 'auteur', 'beschrijving', 'isbn', 'publicatiedatum',
            'kaft_foto_url', 'is_uitgeleend', 'uitgeleend_datum', 'uitgeleend_max_tot'
        ]
        # Check presence
        for attr in required_fields:
            if attr not in kwargs:
                raise BoekCreateMissingAttributeException(f"Missing required attribute: {attr}")
            if attr not in ['uitgeleend_datum','uitgeleend_max_tot'] and kwargs[attr] is None:
                raise BoekCreateMissingAttributeException(f"Missing required attribute: {attr}")

        titel = kwargs['titel']
        auteur = kwargs['auteur']
        beschrijving = kwargs['beschrijving']
        isbn = kwargs['isbn']
        publicatiedatum = kwargs['publicatiedatum']
        kaft_foto_url = kwargs['kaft_foto_url']
        is_uitgeleend = kwargs['is_uitgeleend']
        uitgeleend_datum = kwargs['uitgeleend_datum']
        uitgeleend_max_tot = kwargs['uitgeleend_max_tot']

        # Validaties
        if not isinstance(titel, str):
            raise BoekCreateException("Titel moet een string zijn")
        if not isinstance(auteur, str):
            raise BoekCreateInvalidAuteurException()
        if not isinstance(beschrijving, str):
            raise BoekCreateInvalidBeschrijvingException()
        if not isinstance(isbn, str):
            raise BoekCreateInvalidIsbnException()
        if not isinstance(publicatiedatum, date):
            raise BoekCreateInvalidPublicatiedatumException()
        if not isinstance(kaft_foto_url, str):
            raise BoekCreateInvalidKaftFotoUrlException()
        if not isinstance(is_uitgeleend, bool):
            raise BoekCreateInvalidIsUitgeleendException()
        if uitgeleend_datum is not None and not isinstance(uitgeleend_datum, date):
            raise BoekCreateInvalidUitgeleendDatumException()
        if uitgeleend_max_tot is not None and not isinstance(uitgeleend_max_tot, date):
            raise BoekCreateInvalidUitgeleendMaxTotException()

        sql = (
            "INSERT INTO boeken (titel, auteur, beschrijving, isbn, publicatiedatum, kaft_foto_url, is_uitgeleend, uitgeleend_datum, uitgeleend_max_tot) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        )
        values = (
            titel, auteur, beschrijving, isbn, publicatiedatum, kaft_foto_url, is_uitgeleend, uitgeleend_datum, uitgeleend_max_tot
        )
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(sql, values)
                self.db_connection.commit()
                return cursor.lastrowid
        except Exception as exc:
            self.db_connection.rollback()
            raise BoekCreateDatabaseException(str(exc))
