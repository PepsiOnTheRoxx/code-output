from flask import Flask
from src.api import register_routes
from src.frontend.catalogus import catalogus_blueprint
from src.db import init_db, seed_db

def create_app():
    app = Flask(__name__)

    init_db()
    seed_db()

    register_routes(app)
    app.register_blueprint(catalogus_blueprint, url_prefix='/')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)