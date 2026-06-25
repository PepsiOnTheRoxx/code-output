from flask import Flask
from src.api import register_routes
from src.frontend.views import frontend_blueprint
from src.database import db, init_db
from src.seeder import run_seeder
from src.app_exceptions import *  # importeer custom exceptions als nodig

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    init_db()
    run_seeder()
    register_routes(app)
    app.register_blueprint(frontend_blueprint)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)