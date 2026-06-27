from database import get_connection
from src.services.boekcreate_exceptions import (
    BoekCreateAuteurMissingException,
    BoekCreateBeschrijvingMissingException,
    BoekCreateIsbnMissingException,
    BoekCreatePublicatiedatumInvalidException,
    BoekCreateKaftFotoUrlInvalidException,
    BoekCreateIsUitgeleendInvalidException,
    BoekCreateUitgeleendDatumInvalidException,
    BoekCreateUitgeleendMaxTotInvalidException,
    BoekCreateDuplicateIsbnException,
    BoekCreatePersistenceException,
    BoekCreateValidationException,
    BoekAlreadyExistsException,
    InvalidBoekDataException,
)

import re
from datetime import date, datetime

class BoekRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def exists(self, isbn):
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT COUNT(1) FROM boeken WHERE isbn = ?', (isbn,))
        result = cursor.fetchone()
        return result[0] > 0

    def create(self, auteur, beschrijving, isbn, publicatiedatum, kaft_foto_url,
               is_uitgeleend, uitgeleend_datum, uitgeleend_max_tot):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                '''
                INSERT INTO boeken (
                    auteur, beschrijving, isbn, publicatiedatum,
                    kaft_foto_url, is_uitgeleend, uitgeleend_datum, uitgeleend_max_tot
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    auteur,
                    beschrijving,
                    isbn,
                    publicatiedatum if publicatiedatum is None or isinstance(publicatiedatum, str) else publicatiedatum.isoformat(),
                    kaft_foto_url,
                    int(is_uitgeleend) if type(is_uitgeleend) is bool else is_uitgeleend,
                    uitgeleend_datum if uitgeleend_datum is None or isinstance(uitgeleend_datum, str) else uitgeleend_datum.isoformat(),
                    uitgeleend_max_tot if uitgeleend_max_tot is None or isinstance(uitgeleend_max_tot, str) else uitgeleend_max_tot.isoformat()
                )
            )
            self.db_connection.commit()
            return cursor.lastrowid
        except Exception as exc:
            raise BoekCreatePersistenceException(f'Error bij het aanmaken van boek: {exc}')

class BoekService:
    def __init__(self, db_connection=None):
        if db_connection is None:
            self.db_connection = get_connection()
        else:
            self.db_connection = db_connection
        self.repo = BoekRepository(self.db_connection)

    def _validate_isbn(self, isbn):
        if not isinstance(isbn, str) or len(isbn.strip()) == 0:
            raise BoekCreateIsbnMissingException("ISBN mag niet leeg zijn")
        pattern = r'^97[89][0-9]{10}$'
        if not re.match(pattern, isbn):
            raise BoekCreateIsbnMissingException("ISBN is niet in een geldig formaat")

    def _validate_auteur(self, auteur):
        if not isinstance(auteur, str) or not auteur.strip():
            raise BoekCreateAuteurMissingException("Auteur moet ingevuld zijn")

    def _validate_beschrijving(self, beschrijving):
        if not isinstance(beschrijving, str) or not beschrijving.strip():
            raise BoekCreateBeschrijvingMissingException("Beschrijving moet ingevuld zijn")

    def _validate_publicatiedatum(self, publicatiedatum):
        if publicatiedatum is None:
            raise BoekCreatePublicatiedatumInvalidException("Publicatiedatum moet ingevuld zijn")
        if not (isinstance(publicatiedatum, date) or isinstance(publicatiedatum, datetime)):
            raise BoekCreatePublicatiedatumInvalidException("Publicatiedatum moet een datum zijn")

    def _validate_kaft_foto_url(self, kaft_foto_url):
        if kaft_foto_url is not None:
            if not isinstance(kaft_foto_url, str):
                raise BoekCreateKaftFotoUrlInvalidException("Kaft foto url moet een string zijn")
            if kaft_foto_url and not re.match(r'^https?://', kaft_foto_url):
                raise BoekCreateKaftFotoUrlInvalidException("Kaft foto url moet geldig zijn")

    def _validate_is_uitgeleend(self, is_uitgeleend):
        if not (isinstance(is_uitgeleend, bool)):
            raise BoekCreateIsUitgeleendInvalidException("is_uitgeleend moet een boolean zijn")

    def _validate_uitgeleend_datum(self, uitgeleend_datum):
        if uitgeleend_datum is not None:
            if not (isinstance(uitgeleend_datum, date) or isinstance(uitgeleend_datum, datetime)):
                raise BoekCreateUitgeleendDatumInvalidException("uitgeleend_datum moet een datum of None zijn")

    def _validate_uitgeleend_max_tot(self, uitgeleend_max_tot):
        if uitgeleend_max_tot is not None:
            if not (isinstance(uitgeleend_max_tot, date) or isinstance(uitgeleend_max_tot, datetime)):
                raise BoekCreateUitgeleendMaxTotInvalidException("uitgeleend_max_tot moet een datum of None zijn")

    def create_boek(
        self,
        auteur,
        beschrijving,
        isbn,
        publicatiedatum,
        kaft_foto_url=None,
        is_uitgeleend=False,
        uitgeleend_datum=None,
        uitgeleend_max_tot=None,
    ):
        try:
            self._validate_auteur(auteur)
            self._validate_beschrijving(beschrijving)
            self._validate_isbn(isbn)
            self._validate_publicatiedatum(publicatiedatum)
            self._validate_kaft_foto_url(kaft_foto_url)
            self._validate_is_uitgeleend(is_uitgeleend)
            self._validate_uitgeleend_datum(uitgeleend_datum)
            self._validate_uitgeleend_max_tot(uitgeleend_max_tot)
        except BoekCreateValidationException as e:
            raise InvalidBoekDataException(str(e))

        if self.repo.exists(isbn):
            raise BoekAlreadyExistsException(f"Boek met ISBN {isbn} bestaat al")

        return self.repo.create(
            auteur=auteur,
            beschrijving=beschrijving,
            isbn=isbn,
            publicatiedatum=publicatiedatum,
            kaft_foto_url=kaft_foto_url,
            is_uitgeleend=is_uitgeleend,
            uitgeleend_datum=uitgeleend_datum,
            uitgeleend_max_tot=uitgeleend_max_tot
        )