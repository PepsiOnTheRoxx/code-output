from flask import Flask
# from src.api.catalogus_api import register_routes as register_catalogus_routes  # VERWIJDERD: Bestaat niet
# from src.api.artikel_api import register_routes as register_artikel_routes  # VERWIJDERD: Bestaat niet
# from src.frontend.catalogus_frontend import catalogus_frontend  # VERWIJDERD: Bestaat niet
# from src.db import init_db  # VERWIJDERD: Bestaat niet
# from src.db.seeder import seed_database  # VERWIJDERD: Bestaat niet
# from src.app_exceptions import *  # VERWIJDERD: Bestaat niet

app = Flask(__name__)

# init_db()  # VERWIJDERD
# seed_database()  # VERWIJDERD

# register_catalogus_routes(app)  # VERWIJDERD
# register_artikel_routes(app)    # VERWIJDERD

# app.register_blueprint(catalogus_frontend, url_prefix='/')  # VERWIJDERD

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
