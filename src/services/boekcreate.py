from src.services.boekcreate_exceptions import (
    BoekAlreadyExistsException,
    InvalidBoekDataException,
)

class BoekService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def create_boek(self, titel, auteur, isbn, publicatiejaar, uitgever, pagina_teller, genre, taal):
        required_fields = {
            'titel': str,
            'auteur': str,
            'isbn': str,
            'publicatiejaar': int,
            'uitgever': str,
            'pagina_teller': int,
            'genre': str,
            'taal': str,
        }
        input_data = {
            'titel': titel,
            'auteur': auteur,
            'isbn': isbn,
            'publicatiejaar': publicatiejaar,
            'uitgever': uitgever,
            'pagina_teller': pagina_teller,
            'genre': genre,
            'taal': taal,
        }
        # Check for missing attributes
        for attr, t in required_fields.items():
            if attr not in input_data or input_data[attr] is None:
                raise InvalidBoekDataException(f"Vereist attribuut ontbreekt: {attr}")
            if not isinstance(input_data[attr], t):
                raise InvalidBoekDataException(f"Attribuut {attr} moet type {t.__name__} zijn.")

        cursor = self.db_connection.cursor()
        cursor.execute("SELECT 1 FROM boek WHERE isbn=?", (isbn,))
        if cursor.fetchone() is not None:
            raise BoekAlreadyExistsException(f"Boek met isbn {isbn} bestaat al.")

        insert_sql = (
            "INSERT INTO boek (titel, auteur, isbn, publicatiejaar, uitgever, pagina_teller, genre, taal) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        )
        cursor.execute(
            insert_sql,
            (
                titel,
                auteur,
                isbn,
                publicatiejaar,
                uitgever,
                pagina_teller,
                genre,
                taal
            )
        )
        self.db_connection.commit()