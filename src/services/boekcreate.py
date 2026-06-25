from src.services.boekcreate_exceptions import (
    BoekAlreadyExistsException,
    InvalidBoekDataException,
    DatabaseException
)

class BoekService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def create_boek(self, boek_data):
        vereiste_velden = ['titel', 'auteur', 'isbn', 'uitgever', 'jaar', 'paginas', 'taal', 'genre']
        for veld in vereiste_velden:
            if veld not in boek_data or boek_data[veld] is None or (isinstance(boek_data[veld], str) and not boek_data[veld].strip()):
                raise InvalidBoekDataException(f"Veld '{veld}' ontbreekt of is ongeldig")
        try:
            cursor = self.db_connection.cursor()
            sql = """INSERT INTO boek (titel, auteur, isbn, uitgever, jaar, paginas, taal, genre)
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
                raise DatabaseException("Kon boek niet aanmaken, geen rijen toegevoegd.")
            try:
                self.db_connection.commit()
            except Exception as exc:
                raise DatabaseException(str(exc))
            return True
        except Exception as exc:
            msg = str(exc)
            if "UNIQUE constraint failed" in msg or "unique constraint" in msg.lower():
                raise BoekAlreadyExistsException("Boek met dit ISBN bestaat al.")
            elif isinstance(exc, InvalidBoekDataException):
                raise
            elif isinstance(exc, DatabaseException):
                raise
            else:
                raise DatabaseException(msg)