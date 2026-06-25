from flask import Flask, redirect, url_for
from src.api.boekapi import register_routes as register_boek_routes
from src.frontend.catalogusfrontend import catalogusfrontend_bp
from src.frontend.boekaanpassenfrontend import boekaanpassenfrontend_bp
from src.frontend.boekdetailfrontend import boekdetailfrontend_bp
from src.frontend.boektoevoegenfrontend import boektoevoegenfrontend_bp
from database import init_db
from src.services.boekseeder import BoekSeeder

def create_app():
    app = Flask(__name__)

    # Initialiseer database en seeder
    with app.app_context():
        init_db()
        BoekSeeder().run()

    # Registreer API routes
    register_boek_routes(app)

    # Registreer frontend Blueprints
    app.register_blueprint(catalogusfrontend_bp)
    app.register_blueprint(boekaanpassenfrontend_bp)
    app.register_blueprint(boekdetailfrontend_bp)
    app.register_blueprint(boektoevoegenfrontend_bp)

    # Root redirect naar cataloguspagina
    @app.route("/")
    def home():
        return redirect(url_for("catalogusfrontend.catalogus"))

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
