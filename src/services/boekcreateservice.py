from src.services.boekcreateservice_exceptions import (
    BoekCreateServiceException,
    BoekCreateServiceDatabaseError,
    BoekCreateServiceValidationError,
    BoekCreateServiceMissingAttributeError,
    BoekCreateServiceDuplicateError,
    BoekCreateServiceUnexpectedError,
)
import re

def get_db():
    # Placeholder import. In productie omgeving wordt deze overridden door patching in tests.
    import sqlite3
    return sqlite3.connect('boeken.db')

class BoekCreateService:
    REQUIRED_ATTRIBUTES = [
        'titel',
        'auteur',
        'isbn',
        'uitgever',
        'publicatiejaar',
        'genre',
        'taal',
        'pagina_aantal'
    ]
    
    ISBN_REGEX = re.compile(r"^(97(8|9))?\d{9}(\d|X)$")
    
    def __init__(self):
        pass

    def create_boek(self, boek_data):
        try:
            # Validatie op ontbrekende attributen
            for attr in self.REQUIRED_ATTRIBUTES:
                if attr not in boek_data or boek_data[attr] is None:
                    raise BoekCreateServiceMissingAttributeError(f"Required attribute '{attr}' ontbreekt")

            # ISBN validatie
            isbn = boek_data['isbn']
            if not self.ISBN_REGEX.match(str(isbn)):
                raise BoekCreateServiceValidationError("Ongeldig ISBN formaat")

            db = get_db()
            try:
                cursor = db.execute(
                    """
                    INSERT INTO boeken (titel, auteur, isbn, uitgever, publicatiejaar, genre, taal, pagina_aantal)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        boek_data['titel'],
                        boek_data['auteur'],
                        boek_data['isbn'],
                        boek_data['uitgever'],
                        boek_data['publicatiejaar'],
                        boek_data['genre'],
                        boek_data['taal'],
                        boek_data['pagina_aantal'],
                    ),
                )
                db.commit()
            except Exception as e:
                error_msg = str(e)
                if "UNIQUE constraint failed: boeken.isbn" in error_msg:
                    raise BoekCreateServiceDuplicateError(f"Boek met dit ISBN bestaat al ({boek_data['isbn']})")
                # Andere database gerelateerde fouten
                raise BoekCreateServiceDatabaseError(error_msg)
            # Return het aangemaakte boek als dict (met id als die beschikbaar is)
            boek = dict(boek_data)
            boek['id'] = cursor.lastrowid
            return boek
        except (
            BoekCreateServiceMissingAttributeError,
            BoekCreateServiceValidationError,
            BoekCreateServiceDuplicateError,
            BoekCreateServiceDatabaseError,
        ) as exc:
            raise BoekCreateServiceException(str(exc))
        except Exception as e:
            raise BoekCreateServiceUnexpectedError(str(e))