from flask import Flask, redirect, url_for
from src.api.catalogus_api import register_routes as register_catalogus_routes
from src.api.boek_api import register_routes as register_boek_routes
from src.frontend.catalogus_frontend import catalogus_blueprint
from src.frontend.boek_frontend import boek_blueprint
from src.db import init_db
from src.seeder import seed_db

def create_app():
    app = Flask(__name__)

    # Initialiseer database en seeder
    with app.app_context():
        init_db()
        seed_db()

    # Registreer API routes
    register_catalogus_routes(app)
    register_boek_routes(app)

    # Registreer frontend Blueprints
    app.register_blueprint(catalogus_blueprint)
    app.register_blueprint(boek_blueprint)

    # Root redirect naar cataloguspagina
    @app.route("/")
    def home():
        return redirect(url_for("catalogus.catalogus_pagina"))

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)