from werkzeug.exceptions import NotFound

class BoekNietGevonden(NotFound):
    description = "Boek niet gevonden."

# Register errorhandler so Flask shows the message in the page for tests
from flask import Blueprint, render_template_string
boekdetailfrontend_exceptions_bp = Blueprint('boekdetailfrontend_exceptions', __name__)

@boekdetailfrontend_exceptions_bp.app_errorhandler(BoekNietGevonden)
def handle_boek_niet_gevonden(error):
    return render_template_string('<h1>404</h1>Boek niet gevonden'), 404
