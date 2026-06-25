from src.services.boekcreate_exceptions import (
    BoekCreateUniqueConstraintException,
    BoekCreateValidationException,
    BoekCreateDatabaseException
)

class BoekService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def create_boek(self, boek_data):
        vereiste_velden = ['titel', 'auteur', 'isbn', 'uitgever', 'jaar', 'paginas', 'taal', 'genre']
        for veld in vereiste_velden:
            if veld not in boek_data or boek_data[veld] is None or (isinstance(boek_data[veld], str) and not boek_data[veld].strip()):
                raise BoekCreateValidationException(f"Veld '{veld}' ontbreekt of is ongeldig")
        try:
            cursor = self.db_connection.cursor()
            # Gebruik juiste tabelnaam: 'boeken' i.p.v. 'boek'
            sql = """INSERT INTO boeken (titel, auteur, isbn, uitgever, jaar, paginas, taal, genre)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
            values = [
                boek_data['titel'],
                boek_data['auteur'],
                boek_data['isbn'],
                boek_data['uitgever'],
                boek_data['jaar'],
                boek_data['paginas'],
                boek_data['taal'],
                boek_data['genre']
            ]
            cursor.execute(sql, values)
            if cursor.rowcount != 1:
                raise BoekCreateDatabaseException("Kon boek niet aanmaken, geen rijen toegevoegd.")
            try:
                self.db_connection.commit()
            except Exception as exc:
                raise BoekCreateDatabaseException(str(exc))
            # Return contract: inserted object (id + fields)
            new_id = getattr(cursor, 'lastrowid', None)
            out = boek_data.copy()
            if new_id is not None:
                out['id'] = new_id
            return out
        except Exception as exc:
            msg = str(exc)
            if "UNIQUE constraint failed" in msg or "unique constraint" in msg.lower():
                raise BoekCreateUniqueConstraintException("Boek met dit ISBN bestaat al.")
            elif isinstance(exc, BoekCreateValidationException):
                raise
            elif isinstance(exc, BoekCreateDatabaseException):
                raise
            else:
                raise BoekCreateDatabaseException(msg)

    def get_all_boeken(self):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT * FROM boeken")
            kolommen = [desc[0] for desc in cursor.description]
            return [dict(zip(kolommen, rij)) for rij in cursor.fetchall()]
        except Exception as exc:
            raise BoekCreateDatabaseException(str(exc))

    def get_boek(self, boek_id):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT * FROM boeken WHERE id = ?", (boek_id,))
            rij = cursor.fetchone()
            if rij:
                kolommen = [desc[0] for desc in cursor.description]
                return dict(zip(kolommen, rij))
            else:
                return None
        except Exception as exc:
            raise BoekCreateDatabaseException(str(exc))

    def update_boek(self, boek_id, boek_data):
        gereed_velden = ['titel', 'auteur', 'isbn', 'uitgever', 'jaar', 'paginas', 'taal', 'genre']
        set_paren = ', '.join(f"{veld} = ?" for veld in gereed_velden)
        values = [boek_data[veld] for veld in gereed_velden]
        try:
            cursor = self.db_connection.cursor()
            sql = f"UPDATE boeken SET {set_paren} WHERE id = ?"
            cursor.execute(sql, values + [boek_id])
            if cursor.rowcount != 1:
                raise BoekCreateDatabaseException("Boek niet gevonden of niet gewijzigd.")
            try:
                self.db_connection.commit()
            except Exception as exc:
                raise BoekCreateDatabaseException(str(exc))
            return self.get_boek(boek_id)
        except Exception as exc:
            msg = str(exc)
            if "UNIQUE constraint failed" in msg or "unique constraint" in msg.lower():
                raise BoekCreateUniqueConstraintException("Boek met dit ISBN bestaat al.")
            elif isinstance(exc, BoekCreateValidationException):
                raise
            elif isinstance(exc, BoekCreateDatabaseException):
                raise
            else:
                raise BoekCreateDatabaseException(msg)

    def delete_boek(self, boek_id):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("DELETE FROM boeken WHERE id = ?", (boek_id,))
            if cursor.rowcount != 1:
                raise BoekCreateDatabaseException("Boek niet gevonden om te verwijderen.")
            try:
                self.db_connection.commit()
            except Exception as exc:
                raise BoekCreateDatabaseException(str(exc))
            return True
        except Exception as exc:
            raise BoekCreateDatabaseException(str(exc))
