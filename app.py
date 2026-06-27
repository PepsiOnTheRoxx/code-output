from flask import Flask
from src.frontend.catalogusfrontend import catalogusfrontend_bp
from src.api.boekapi import register_routes
from database import init_db, seed_db
# Let op: src.app_exceptions bestaat niet; eventueel weghalen of implementeer indien nodig

app = Flask(__name__)

init_db()
# seed_db() bestaat niet in database.py. Indien seed_db() elders is, importeer correct of implementeer. Dus hier voorlopig uit commentaar:
# seed_db()

register_routes(app)

app.register_blueprint(catalogusfrontend_bp, url_prefix='/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
