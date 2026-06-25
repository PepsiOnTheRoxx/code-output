from flask import Flask, request, jsonify
from src.api.boekserviceapi_exceptions import BoekNietGevondenException, OngeldigeBoekDataException

app = Flask(__name__)

# boek_service wordt gepatcht in de unittests
boek_service = None

@app.route('/boeken', methods=['POST'])
def creeer_boek():
    boek_data = request.get_json()
    try:
        resultaat = boek_service.creeer_boek(boek_data)
        return jsonify(resultaat), 201
    except OngeldigeBoekDataException as ex:
        return jsonify({"beschrijving": str(ex)}), 400

@app.route('/boeken/<int:boek_id>', methods=['GET'])
def lees_boek(boek_id):
    try:
        resultaat = boek_service.lees_boek(boek_id)
        return jsonify(resultaat), 200
    except BoekNietGevondenException as ex:
        return jsonify({"beschrijving": str(ex)}), 404

@app.route('/boeken/<int:boek_id>', methods=['PUT'])
def update_boek(boek_id):
    boek_data = request.get_json()
    try:
        resultaat = boek_service.update_boek(boek_id, boek_data)
        return jsonify(resultaat), 200
    except BoekNietGevondenException as ex:
        return jsonify({"beschrijving": str(ex)}), 404
    except OngeldigeBoekDataException as ex:
        return jsonify({"beschrijving": str(ex)}), 400

@app.route('/boeken/<int:boek_id>', methods=['DELETE'])
def verwijder_boek(boek_id):
    try:
        boek_service.verwijder_boek(boek_id)
        return '', 204
    except BoekNietGevondenException as ex:
        return jsonify({"beschrijving": str(ex)}), 404
