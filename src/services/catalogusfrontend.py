from src.services.catalogusfrontend_exceptions import CatalogusDataError, CatalogusNavigationError

class CatalogusTemplate:
    def __init__(self, boek_service, navigatie_service):
        self.boek_service = boek_service
        self.navigatie_service = navigatie_service
        self.boeken = []
    
    def laad_boeken(self):
        try:
            self.boeken = self.boek_service.haal_boeken_op()
        except Exception as e:
            raise CatalogusDataError(f"Fout bij ophalen boeken: {e}")
    
    def render_boek_lijst(self):
        if not self.boeken:
            return "<p>Geen boeken gevonden.</p>"
        html = "<ul class='catalogus-lijst'>"
        for boek in self.boeken:
            html += f"""
                <li class='boek-item'>
                    <div class='boek-kaft'>
                        <img src='{boek.kaft_url}' alt='Kaft van {boek.titel}' />
                    </div>
                    <div class='boek-info'>
                        <h3>{boek.titel}</h3>
                        <p>Auteur: {boek.auteur}</p>
                        <p>Status: {"Beschikbaar" if boek.beschikbaar else "Uitgeleend"}</p>
                    </div>
                    <div class='boek-acties'>
                        <a href='{self.navigatie_service.genereer_boek_url(boek.id)}'>Bekijk details</a>
                        <a href='{self.navigatie_service.genereer_uitleen_url(boek.id)}'>{"Uitleen" if boek.beschikbaar else "Reserveer"}</a>
                    </div>
                </li>
            """
        html += "</ul>"
        html += self.render_navigatie()
        return html

    def render_navigatie(self):
        try:
            links = [
                ("Home", self.navigatie_service.genereer_home_url()),
                ("Mijn boeken", self.navigatie_service.genereer_mijn_boeken_url()),
                ("Reserveringen", self.navigatie_service.genereer_reserveringen_url())
            ]
        except Exception as e:
            raise CatalogusNavigationError(f"Fout met navigatie genereren: {e}")
        html = "<nav class='catalogus-navigatie'>"
        for naam, url in links:
            html += f"<a href='{url}'>{naam}</a>"
        html += "</nav>"
        return html

    def render_pagina(self):
        self.laad_boeken()
        pagina_html = "<div class='catalogus-pagina'>"
        pagina_html += "<h1>Catalogus</h1>"
        pagina_html += self.render_boek_lijst()
        pagina_html += "</div>"
        return pagina_html