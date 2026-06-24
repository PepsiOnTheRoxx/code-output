from flask import Flask, jsonify, request, abort

from src.api.vtproceseigenaarrelatieapi_exceptions import (
    ProceseigenaarRelatieNotFoundError,
    InvalidProceseigenaarRelatieData
)

app = Flask(__name__)

def get_proceseigenaarrelatie_by_id(relatie_id):
    # Dummy logic to be replaced by actual implementation
    raise NotImplementedError

def create_proceseigenaarrelatie(data):
    # Dummy logic to be replaced by actual implementation
    raise NotImplementedError

def delete_proceseigenaarrelatie(relatie_id):
    # Dummy logic to be replaced by actual implementation
    raise NotImplementedError

def list_proceseigenaarrelaties():
    # Dummy logic to be replaced by actual implementation
    raise NotImplementedError

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