import os
from flask import Flask
from src.app_exceptions import AppInitializationException

def register_blueprints(app):
    from src.api.v1.users import users_bp
    from src.api.v1.auth import auth_bp
    from src.api.v1.products import products_bp

    app.register_blueprint(users_bp, url_prefix='/api/v1/users')
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(products_bp, url_prefix='/api/v1/products')

def create_app():
    app = Flask(__name__)
    try:
        app.config.from_pyfile('config.py')
    except Exception as exc:
        raise AppInitializationException(f"Fout bij laden config: {exc}")

    try:
        register_blueprints(app)
    except Exception as exc:
        raise AppInitializationException(f"Fout bij registratie blueprints: {exc}")

    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)