from flask import Flask, jsonify, request

from src.api.vtproceseigenaarrelatieapi_exceptions import (
    ProceseigenaarRelatieNotFoundError,
    InvalidProceseigenaarRelatieData
)

app = Flask(__name__)

def get_proceseigenaarrelatie_by_id(relatie_id):
    # Example dummy data
    if relatie_id == 1:
        return {'id': 1, 'proceseigenaar_id': 123, 'proces_id': 456}
    raise ProceseigenaarRelatieNotFoundError

def create_proceseigenaarrelatie(data):
    if not data or 'proceseigenaar_id' not in data or 'proces_id' not in data:
        raise InvalidProceseigenaarRelatieData
    # Example, always return new ID 2 in test
    return {'id': 2, 'proceseigenaar_id': data['proceseigenaar_id'], 'proces_id': data['proces_id']}

def delete_proceseigenaarrelatie(relatie_id):
    if relatie_id != 1:
        raise ProceseigenaarRelatieNotFoundError
    return None

def list_proceseigenaarrelaties():
    return [
        {'id': 1, 'proceseigenaar_id': 123, 'proces_id': 456},
        {'id': 2, 'proceseigenaar_id': 124, 'proces_id': 457}
    ]

@app.route('/vt/proceseigenaarrelatie/<int:relatie_id>', methods=['GET'])
def get_proceseigenaarrelatie(relatie_id):
    try:
        obj = get_proceseigenaarrelatie_by_id(relatie_id)
        return jsonify(obj), 200
    except ProceseigenaarRelatieNotFoundError:
        return '', 404

@app.route('/vt/proceseigenaarrelatie', methods=['POST'])
def post_proceseigenaarrelatie():
    try:
        obj = create_proceseigenaarrelatie(request.get_json())
        return jsonify(obj), 201
    except InvalidProceseigenaarRelatieData:
        return '', 400

@app.route('/vt/proceseigenaarrelatie/<int:relatie_id>', methods=['DELETE'])
def delete_proceseigenaarrelatie_route(relatie_id):
    try:
        delete_proceseigenaarrelatie(relatie_id)
        return '', 204
    except ProceseigenaarRelatieNotFoundError:
        return '', 404

@app.route('/vt/proceseigenaarrelatie', methods=['GET'])
def list_proceseigenaarrelaties_route():
    result = list_proceseigenaarrelaties()
    return jsonify(result), 200
