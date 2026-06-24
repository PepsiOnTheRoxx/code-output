from flask import request, jsonify

from src.api.vtbronnenrelatieapi_exceptions import (
    VTBronnenRelatieNotFoundException,
    VTBronnenRelatieValidationException,
)

class VTBronnenRelatieAPI:
    _relaties = []
    _next_id = 1

    def register_routes(self, app):
        @app.route('/vtbronnenrelatie', methods=['GET'])
        def get_all_relaties_route():
            try:
                return jsonify(self.get_all_relaties()), 200
            except Exception as ex:
                return jsonify({'error': str(ex)}), 500

        @app.route('/vtbronnenrelatie/<int:relatie_id>', methods=['GET'])
        def get_relatie_route(relatie_id):
            try:
                return jsonify(self.get_relatie_by_id(relatie_id)), 200
            except VTBronnenRelatieNotFoundException as ex:
                return jsonify({'error': str(ex)}), 404
            except Exception as ex:
                return jsonify({'error': str(ex)}), 500

        @app.route('/vtbronnenrelatie', methods=['POST'])
        def post_relatie_route():
            try:
                data = request.json
                return jsonify(self.create_relatie(data)), 201
            except VTBronnenRelatieValidationException as ex:
                return jsonify({'error': str(ex)}), 400
            except Exception as ex:
                return jsonify({'error': str(ex)}), 500

        @app.route('/vtbronnenrelatie/<int:relatie_id>', methods=['PUT'])
        def put_relatie_route(relatie_id):
            try:
                data = request.json
                return jsonify(self.update_relatie(relatie_id, data)), 200
            except VTBronnenRelatieNotFoundException as ex:
                return jsonify({'error': str(ex)}), 404
            except VTBronnenRelatieValidationException as ex:
                return jsonify({'error': str(ex)}), 400
            except Exception as ex:
                return jsonify({'error': str(ex)}), 500

        @app.route('/vtbronnenrelatie/<int:relatie_id>', methods=['DELETE'])
        def delete_relatie_route(relatie_id):
            try:
                self.delete_relatie(relatie_id)
                return '', 204
            except VTBronnenRelatieNotFoundException as ex:
                return jsonify({'error': str(ex)}), 404
            except Exception as ex:
                return jsonify({'error': str(ex)}), 500

    def get_all_relaties(self):
        return list(self.__class__._relaties)

    def get_relatie_by_id(self, relatie_id):
        for relatie in self.__class__._relaties:
            if relatie['id'] == relatie_id:
                return dict(relatie)
        raise VTBronnenRelatieNotFoundException("Not found")

    def create_relatie(self, data):
        naam = data.get('naam')
        if not naam or not isinstance(naam, str) or not naam.strip():
            raise VTBronnenRelatieValidationException('Validatiefout')
        relatie = {'id': self.__class__._next_id, 'naam': naam}
        self.__class__._relaties.append(relatie)
        self.__class__._next_id += 1
        return dict(relatie)

    def update_relatie(self, relatie_id, data):
        for idx, relatie in enumerate(self.__class__._relaties):
            if relatie['id'] == relatie_id:
                naam = data.get('naam')
                if not naam or not isinstance(naam, str) or not naam.strip():
                    raise VTBronnenRelatieValidationException('Validatiefout')
                updated = dict(relatie)
                updated['naam'] = naam
                self.__class__._relaties[idx] = updated
                return dict(updated)
        raise VTBronnenRelatieNotFoundException('Niet gevonden')

    def delete_relatie(self, relatie_id):
        for idx, relatie in enumerate(self.__class__._relaties):
            if relatie['id'] == relatie_id:
                del self.__class__._relaties[idx]
                return True
        raise VTBronnenRelatieNotFoundException('Verwijderen mislukt')
