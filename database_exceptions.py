class DatabaseSetupException(Exception):
    """Algemene exception voor DatabaseSetup component."""
    pass

class DatabaseConnectionError(DatabaseSetupException):
    """Fout bij verbinding maken met de database."""
    pass

class DatabaseTableCreationError(DatabaseSetupException):
    """Fout bij het aanmaken van de Boek tabel."""
    pass

class BoekAttribuutFout(DatabaseSetupException):
    """Probleem met attributen van de Boek tabel."""
    pass

class BoekAuteurMissingError(BoekAttribuutFout):
    """Het 'auteur' attribuut ontbreekt of is ongeldig."""
    pass

class BoekBeschrijvingMissingError(BoekAttribuutFout):
    """Het 'beschrijving' attribuut ontbreekt of is ongeldig."""
    pass

class BoekIsbnMissingError(BoekAttribuutFout):
    """Het 'isbn' attribuut ontbreekt of is ongeldig."""
    pass

class BoekTitelMissingError(BoekAttribuutFout):
    """Het 'titel' attribuut ontbreekt of is ongeldig."""
    pass

class BoekKaftFotoUrlError(BoekAttribuutFout):
    """Het 'kaft_foto_url' attribuut ontbreekt of is ongeldig."""
    pass

class BoekPublicatiedatumError(BoekAttribuutFout):
    """Het 'publicatiedatum' attribuut ontbreekt of bevat een foutief formaat."""
    pass

class BoekIsUitgeleendTypeError(BoekAttribuutFout):
    """Het 'is_uitgeleend' attribuut is niet van het type boolean."""
    pass

class BoekUitgeleendDatumError(BoekAttribuutFout):
    """Het 'uitgeleend_datum' attribuut ontbreekt of bevat een foutief formaat."""
    pass

class BoekUitgeleendMaxTotError(BoekAttribuutFout):
    """Het 'uitgeleend_max_tot' attribuut ontbreekt of bevat een foutief formaat."""
    pass