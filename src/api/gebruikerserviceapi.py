from flask import Flask, request, jsonify
from src.api.gebruikerserviceapi_exceptions import (
    GebruikerNotFoundException,
    GebruikerValidationException,
)
app = Flask(__name__)

class GebruikerService:
    def get_gebruiker(self, gebruiker_id):
        pass

    def create_gebruiker(self, data):
        pass

    def delete_gebruiker(self, gebruiker_id):
        pass

@app.route("/gebruiker/<int:gebruiker_id>", methods=["GET"])
def get_gebruiker(gebruiker_id):
    service = GebruikerService()
    try:
        gebruiker = service.get_gebruiker(gebruiker_id)
        return jsonify(gebruiker)
    except GebruikerNotFoundException as e:
        raise e

@app.route("/gebruiker", methods=["POST"])
def create_gebruiker():
    data = request.get_json()
    service = GebruikerService()
    try:
        gebruiker = service.create_gebruiker(data)
        return jsonify(gebruiker)
    except GebruikerValidationException as e:
        raise e

@app.route("/gebruiker/<int:gebruiker_id>", methods=["DELETE"])
def delete_gebruiker(gebruiker_id):
    service = GebruikerService()
    try:
        result = service.delete_gebruiker(gebruiker_id)
        return jsonify(result)
    except GebruikerNotFoundException as e:
        raise e