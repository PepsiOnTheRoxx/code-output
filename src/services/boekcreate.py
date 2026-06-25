from src.services.boekcreate_exceptions import (
    BoekCreateDuplicateException,
    BoekCreateInvalidAttributeException,
)

class BoekService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def create_boek(self, **kwargs):
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
        # Controleer op ontbrekende of onjuiste attributen
        for attr, t in required_fields.items():
            if attr not in kwargs or kwargs[attr] is None:
                raise BoekCreateInvalidAttributeException(f"Vereist attribuut ontbreekt: {attr}")
            if not isinstance(kwargs[attr], t):
                raise BoekCreateInvalidAttributeException(f"Attribuut {attr} moet type {t.__name__} zijn.")

        cursor = self.db_connection.cursor()
        cursor.execute("SELECT 1 FROM boek WHERE isbn=?", (kwargs['isbn'],))
        if cursor.fetchone() is not None:
            raise BoekCreateDuplicateException(f"Boek met isbn {kwargs['isbn']} bestaat al.")

        insert_sql = (
            "INSERT INTO boek (titel, auteur, isbn, publicatiejaar, uitgever, pagina_teller, genre, taal) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        )
        cursor.execute(
            insert_sql,
            (
                kwargs['titel'],
                kwargs['auteur'],
                kwargs['isbn'],
                kwargs['publicatiejaar'],
                kwargs['uitgever'],
                kwargs['pagina_teller'],
                kwargs['genre'],
                kwargs['taal']
            )
        )
        self.db_connection.commit()
