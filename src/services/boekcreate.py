from datetime import date
from database import get_connection
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

class BoekService:
    def __init__(self, db_connection=None):
        if db_connection is None:
            self.db_connection = get_connection()
        else:
            self.db_connection = db_connection

    def create_boek(
        self,
        auteur,
        beschrijving,
        isbn,
        publicatiedatum,
        kaft_foto_url,
        is_uitgeleend,
        uitgeleend_datum,
        uitgeleend_max_tot
    ):
        required_fields = [
            "auteur", "beschrijving", "isbn", "publicatiedatum",
            "kaft_foto_url", "is_uitgeleend", "uitgeleend_datum", "uitgeleend_max_tot"
        ]
        locals_data = locals()
        for attr in required_fields:
            if attr not in locals_data or (attr != "uitgeleend_datum" and attr != "uitgeleend_max_tot" and locals_data[attr] is None):
                raise BoekCreateMissingAttributeException(f"Missing required attribute: {attr}")

        if not isinstance(auteur, str):
            raise BoekCreateInvalidAuteurException("auteur is not a string")
        if not isinstance(beschrijving, str):
            raise BoekCreateInvalidBeschrijvingException("beschrijving is not a string")
        if not isinstance(isbn, str):
            raise BoekCreateInvalidIsbnException("isbn is not a string")
        if not (isinstance(publicatiedatum, date)):
            raise BoekCreateInvalidPublicatiedatumException("publicatiedatum is not a date")
        if not isinstance(kaft_foto_url, str):
            raise BoekCreateInvalidKaftFotoUrlException("kaft_foto_url is not a string")
        if not isinstance(is_uitgeleend, bool):
            raise BoekCreateInvalidIsUitgeleendException("is_uitgeleend is not a boolean")
        if uitgeleend_datum is not None and not isinstance(uitgeleend_datum, date):
            raise BoekCreateInvalidUitgeleendDatumException("uitgeleend_datum is not a date or None")
        if uitgeleend_max_tot is not None and not isinstance(uitgeleend_max_tot, date):
            raise BoekCreateInvalidUitgeleendMaxTotException("uitgeleend_max_tot is not a date or None")

        sql = (
            "INSERT INTO boeken (auteur, beschrijving, isbn, publicatiedatum, kaft_foto_url, is_uitgeleend, uitgeleend_datum, uitgeleend_max_tot) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        )
        params = (
            auteur,
            beschrijving,
            isbn,
            publicatiedatum,
            kaft_foto_url,
            is_uitgeleend,
            uitgeleend_datum,
            uitgeleend_max_tot
        )
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(sql, params)
                boek_id = cursor.lastrowid
            self.db_connection.commit()
            return boek_id
        except Exception as ex:
            raise BoekCreateDatabaseException("Database error during Boek create") from ex