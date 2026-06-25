from src.frontend.boektoevoegenfrontend_exceptions import BoekToevoegenFout, BoekAPINietBeschikbaar

class BoekToevoegenPage:
    def __init__(self, db_connection, boek_api):
        self.db_connection = db_connection
        self.boek_api = boek_api

    def render_formulier(self):
        return '''
            <form method="POST" action="/boeken/toevoegen">
                Titel: <input type="text" name="titel" required><br>
                Auteur: <input type="text" name="auteur" required><br>
                ISBN: <input type="text" name="isbn" required><br>
                Publicatiedatum: <input type="date" name="publicatiedatum"><br>
                Genre: <input type="text" name="genre"><br>
                <input type="submit" value="Toevoegen">
            </form>
            <a href="/catalogus">Terug naar catalogus</a>
        '''

    def process_formulier(self, form_data):
        try:
            boek_data = {
                "titel": form_data["titel"],
                "auteur": form_data["auteur"],
                "isbn": form_data["isbn"],
                "publicatiedatum": form_data.get("publicatiedatum"),
                "genre": form_data.get("genre")
            }
            nieuw_boek_id = self.boek_api.voeg_boek_toe(boek_data)
        except Exception as e:
            raise BoekToevoegenFout("Kon boek niet toevoegen") from e

        return f'/boeken/{nieuw_boek_id}'

    def handle_request(self, request):
        if request.method == "GET":
            return self.render_formulier()
        elif request.method == "POST":
            try:
                redirect_url = self.process_formulier(request.form)
            except BoekToevoegenFout:
                return self.render_formulier() + "<div>Fout bij toevoegen boek.</div>"
            return f'<meta http-equiv="refresh" content="0;url={redirect_url}">'
        else:
            raise BoekAPINietBeschikbaar("Onbekende request methode")