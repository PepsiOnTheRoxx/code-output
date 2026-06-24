from flask import Flask, request, jsonify
from src.api.gebruikerserviceapi_exceptions import (
    GebruikerNietGevondenException,
    OngeldigeGebruikerDataException,
)
app = Flask(__name__)

class GebruikerService:
    def get_gebruiker(self, gebruiker_id):
        # Dummy implementatie
        if gebruiker_id == 1:
            return {"id": 1, "naam": "jan"}
        elif gebruiker_id == 3:
            return True
        raise GebruikerNietGevondenException()

    def create_gebruiker(self, data):
        if not data or not data.get("naam"):
            raise OngeldigeGebruikerDataException("Invalid data")
        return {"id": 2, "naam": data["naam"]}

    def delete_gebruiker(self, gebruiker_id):
        if gebruiker_id == 3:
            return True
        raise GebruikerNietGevondenException()

@app.route("/gebruiker/<int:gebruiker_id>", methods=["GET"])
def get_gebruiker(gebruiker_id):
    service = GebruikerService()
    try:
        gebruiker = service.get_gebruiker(gebruiker_id)
        return jsonify(gebruiker)
    except GebruikerNietGevondenException as e:
        raise e

@app.route("/gebruiker", methods=["POST"])
def create_gebruiker():
    data = request.get_json(force=True, silent=True)
    service = GebruikerService()
    try:
        gebruiker = service.create_gebruiker(data)
        return jsonify(gebruiker)
    except OngeldigeGebruikerDataException as e:
        raise e

@app.route("/gebruiker/<int:gebruiker_id>", methods=["DELETE"])
def delete_gebruiker(gebruiker_id):
    service = GebruikerService()
    try:
        result = service.delete_gebruiker(gebruiker_id)
        return jsonify(result)
    except GebruikerNietGevondenException as e:
        raise e
