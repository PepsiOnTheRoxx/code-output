import pytest
from flask import Flask, json
from unittest.mock import patch, MagicMock
from src.api.vtbehandelaarrelatieapi import VTBehandelaarRelatieAPI
from src.api.vtbehandelaarrelatieapi_exceptions import VTBehandelaarRelatieNotFound, VTBehandelaarRelatieInvalidData

@pytest.fixture
def app():
    app = Flask(__name__)
    api = VTBehandelaarRelatieAPI()
    api.register_routes(app)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_behandelaarrelatie_success(client):
    with patch('src.api.vtbehandelaarrelatieapi.VTBehandelaarRelatieAPI.get_behandelaarrelatie', return_value={'id': 1, 'naam': 'Jan'}) as mock_get:
        response = client.get('/behandelaarrelatie/1')
        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == 1
        assert data['naam'] == 'Jan'
        mock_get.assert_called_once_with(1)

def test_get_behandelaarrelatie_not_found(client):
    with patch('src.api.vtbehandelaarrelatieapi.VTBehandelaarRelatieAPI.get_behandelaarrelatie', side_effect=VTBehandelaarRelatieNotFound):
        response = client.get('/behandelaarrelatie/42')
        assert response.status_code == 404

def test_create_behandelaarrelatie_success(client):
    payload = {'naam': 'Piet'}
    with patch('src.api.vtbehandelaarrelatieapi.VTBehandelaarRelatieAPI.create_behandelaarrelatie', return_value={'id': 2, 'naam': 'Piet'}) as mock_create:
        response = client.post('/behandelaarrelatie', data=json.dumps(payload), content_type='application/json')
        assert response.status_code == 201
        data = response.get_json()
        assert data['id'] == 2
        assert data['naam'] == 'Piet'
        mock_create.assert_called_once_with(payload)

def test_create_behandelaarrelatie_invalid_data(client):
    payload = {'naam': ''}
    with patch('src.api.vtbehandelaarrelatieapi.VTBehandelaarRelatieAPI.create_behandelaarrelatie', side_effect=VTBehandelaarRelatieInvalidData):
        response = client.post('/behandelaarrelatie', data=json.dumps(payload), content_type='application/json')
        assert response.status_code == 400

def test_update_behandelaarrelatie_success(client):
    payload = {'naam': 'Klaas'}
    with patch('src.api.vtbehandelaarrelatieapi.VTBehandelaarRelatieAPI.update_behandelaarrelatie', return_value={'id': 3, 'naam': 'Klaas'}) as mock_update:
        response = client.put('/behandelaarrelatie/3', data=json.dumps(payload), content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == 3
        assert data['naam'] == 'Klaas'
        mock_update.assert_called_once_with(3, payload)

def test_update_behandelaarrelatie_not_found(client):
    payload = {'naam': 'Onbekend'}
    with patch('src.api.vtbehandelaarrelatieapi.VTBehandelaarRelatieAPI.update_behandelaarrelatie', side_effect=VTBehandelaarRelatieNotFound):
        response = client.put('/behandelaarrelatie/999', data=json.dumps(payload), content_type='application/json')
        assert response.status_code == 404

def test_delete_behandelaarrelatie_success(client):
    with patch('src.api.vtbehandelaarrelatieapi.VTBehandelaarRelatieAPI.delete_behandelaarrelatie', return_value=None) as mock_delete:
        response = client.delete('/behandelaarrelatie/5')
        assert response.status_code == 204
        mock_delete.assert_called_once_with(5)

def test_delete_behandelaarrelatie_not_found(client):
    with patch('src.api.vtbehandelaarrelatieapi.VTBehandelaarRelatieAPI.delete_behandelaarrelatie', side_effect=VTBehandelaarRelatieNotFound):
        response = client.delete('/behandelaarrelatie/888')
        assert response.status_code == 404