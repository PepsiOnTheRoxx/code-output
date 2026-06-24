import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, jsonify
from src.api.vtbronnenrelatieapi import (
    VTBronnenRelatieAPI,
)
from src.api.vtbronnenrelatieapi_exceptions import (
    VTBronnenRelatieNotFoundException,
    VTBronnenRelatieValidationException,
)

@pytest.fixture(autouse=True)
def reset_relatie_state():
    # Reset the mock data before each test so tests are independent
    VTBronnenRelatieAPI._relaties = []
    VTBronnenRelatieAPI._next_id = 1

@pytest.fixture
def app():
    app = Flask(__name__)
    api = VTBronnenRelatieAPI()
    api.register_routes(app)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_relatie_success(client):
    relatie_data = {'id': 1, 'naam': 'TestRelatie'}
    with patch('src.api.vtbronnenrelatieapi.VTBronnenRelatieAPI.get_relatie_by_id', return_value=relatie_data):
        response = client.get('/vtbronnenrelatie/1')
        assert response.status_code == 200
        assert response.get_json() == relatie_data

def test_get_relatie_not_found(client):
    with patch('src.api.vtbronnenrelatieapi.VTBronnenRelatieAPI.get_relatie_by_id', side_effect=VTBronnenRelatieNotFoundException("Not found")):
        response = client.get('/vtbronnenrelatie/9999')
        assert response.status_code == 404
        assert response.get_json()['error'] == 'Not found'

def test_post_relatie_success(client):
    post_data = {'naam': 'NieuweRelatie'}
    created_data = {'id': 2, 'naam': 'NieuweRelatie'}
    with patch('src.api.vtbronnenrelatieapi.VTBronnenRelatieAPI.create_relatie', return_value=created_data):
        response = client.post('/vtbronnenrelatie', json=post_data)
        assert response.status_code == 201
        assert response.get_json() == created_data

def test_post_relatie_validation_error(client):
    post_data = {'naam': ''}  # ongeldig, leeg veld
    with patch('src.api.vtbronnenrelatieapi.VTBronnenRelatieAPI.create_relatie', side_effect=VTBronnenRelatieValidationException('Validatiefout')):
        response = client.post('/vtbronnenrelatie', json=post_data)
        assert response.status_code == 400
        assert response.get_json()['error'] == 'Validatiefout'

def test_put_relatie_success(client):
    put_data = {'naam': 'Aangepast'}
    updated_data = {'id': 3, 'naam': 'Aangepast'}
    with patch('src.api.vtbronnenrelatieapi.VTBronnenRelatieAPI.update_relatie', return_value=updated_data):
        response = client.put('/vtbronnenrelatie/3', json=put_data)
        assert response.status_code == 200
        assert response.get_json() == updated_data

def test_put_relatie_not_found(client):
    put_data = {'naam': 'BestaatNiet'}
    with patch('src.api.vtbronnenrelatieapi.VTBronnenRelatieAPI.update_relatie', side_effect=VTBronnenRelatieNotFoundException("Niet gevonden")):
        response = client.put('/vtbronnenrelatie/9999', json=put_data)
        assert response.status_code == 404
        assert response.get_json()['error'] == 'Niet gevonden'

def test_delete_relatie_success(client):
    with patch('src.api.vtbronnenrelatieapi.VTBronnenRelatieAPI.delete_relatie', return_value=True):
        response = client.delete('/vtbronnenrelatie/5')
        assert response.status_code == 204

def test_delete_relatie_not_found(client):
    with patch('src.api.vtbronnenrelatieapi.VTBronnenRelatieAPI.delete_relatie', side_effect=VTBronnenRelatieNotFoundException("Verwijderen mislukt")):
        response = client.delete('/vtbronnenrelatie/9999')
        assert response.status_code == 404
        assert response.get_json()['error'] == 'Verwijderen mislukt'

def test_get_all_relatie(client):
    relaties = [
        {'id': 1, 'naam': 'Relatie1'},
        {'id': 2, 'naam': 'Relatie2'},
    ]
    with patch('src.api.vtbronnenrelatieapi.VTBronnenRelatieAPI.get_all_relaties', return_value=relaties):
        response = client.get('/vtbronnenrelatie')
        assert response.status_code == 200
        assert response.get_json() == relaties
