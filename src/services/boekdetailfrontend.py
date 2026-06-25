from src.services.boekdetailfrontend_exceptions import BoekNietGevondenException, NavigatieFoutException

class BoekDetailTemplate:
    def __init__(self, boek_repository, uitleen_service, router):
        self.boek_repository = boek_repository
        self.uitleen_service = uitleen_service
        self.router = router

    def render(self, boek_id):
        boek = self.boek_repository.haal_boek_op(boek_id)
        if boek is None:
            raise BoekNietGevondenException(f"Geen boek gevonden met id {boek_id}")
        uitleeninformatie = self.uitleen_service.haal_uitleeninformatie_op(boek_id)
        pagina = {
            'titel': boek.titel,
            'auteur': boek.auteur,
            'isbn': boek.isbn,
            'categorie': boek.categorie,
            'beschikbaar': boek.beschikbaar,
            'uitleeninformatie': uitleeninformatie,
        }
        return pagina

    def navigeren_naar_overzicht(self):
        try:
            return self.router.redirect('/boeken')
        except Exception as e:
            raise NavigatieFoutException("Fout tijdens navigatie naar overzichtspagina") from e

    def navigeren_naar_uitleen(self, boek_id):
        try:
            return self.router.redirect(f'/boeken/{boek_id}/uitleen')
        except Exception as e:
            raise NavigatieFoutException("Fout tijdens navigatie naar uitleenpagina") from e