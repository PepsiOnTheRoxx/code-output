from flask import Flask
from src.api import register_routes
from src.frontend.views import frontend_blueprint
from src.db import init_db, seed_db
from src.app_exceptions import *

app = Flask(__name__)

register_routes(app)
app.register_blueprint(frontend_blueprint)

with app.app_context():
    init_db()
    seed_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)