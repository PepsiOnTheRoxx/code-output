from flask import Flask
from src.api.catalogus_api import register_routes as register_catalogus_routes
from src.api.artikel_api import register_routes as register_artikel_routes
from src.frontend.catalogus_frontend import catalogus_frontend
from src.db import init_db
from src.db.seeder import seed_database
from src.app_exceptions import *

app = Flask(__name__)

init_db()
seed_database()

register_catalogus_routes(app)
register_artikel_routes(app)

app.register_blueprint(catalogus_frontend, url_prefix='/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)