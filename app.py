from flask import Flask
from src.frontend.catalogus import catalogus_blueprint
from src.api.routes import register_routes
from src.db import init_db, seed_db
from src.app_exceptions import *

app = Flask(__name__)

init_db()
seed_db()

register_routes(app)

app.register_blueprint(catalogus_blueprint, url_prefix='/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)