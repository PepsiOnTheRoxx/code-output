from flask import Flask, send_from_directory
import os
from src.api.catalogus import register_routes as register_catalogus_routes
from src.api.product import register_routes as register_product_routes
from src.api.order import register_routes as register_order_routes
from src.database import init_db, is_db_empty
from src.seeder import seed_db
from src.app_exceptions import *
from pathlib import Path

app = Flask(__name__, static_folder="frontend/catalogus", static_url_path="")

def setup_app(app):
    # Register all routes
    register_catalogus_routes(app)
    register_product_routes(app)
    register_order_routes(app)

    # Initialize the database
    db_path = os.path.join(os.path.dirname(__file__), "database", "app.db")
    init_db(db_path)

    # Run seeder if database is empty
    if is_db_empty(db_path):
        seed_db(db_path)

setup_app(app)

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    # Ensure database folder exists
    db_dir = os.path.join(os.path.dirname(__file__), "database")
    Path(db_dir).mkdir(exist_ok=True)
    app.run(host="0.0.0.0", port=5000, debug=True)