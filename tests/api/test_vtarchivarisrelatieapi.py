import pytest
from unittest.mock import patch, MagicMock
from src.api.vtarchivarisrelatieapi import VTArchivarisRelatieAPI
from src.api.vtarchivarisrelatieapi_exceptions import VTArchivarisRelatieNotFound, VTArchivarisRelatieValidationError

@pytest.fixture
def client():
    app = VTArchivarisRelatieAPI().app
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_archivarisrelatie_success(client):
    with patch('src.api.vtarchivarisrelatieapi.VTArchivarisRelatieService') as mock_service:
        instance = mock_service.return_value
        instance.get_relatie.return_value = {'id': 1, 'naam': 'Jan', 'archief': '12345'}
        response = client.get('/archivarisrelatie/1')
        assert response.status_code == 200
        assert response.json == {'id': 1, 'naam': 'Jan', 'archief': '12345'}
        instance.get_relatie.assert_called_once_with(1)

def test_get_archivarisrelatie_not_found(client):
    with patch('src.api.vtarchivarisrelatieapi.VTArchivarisRelatieService') as mock_service:
        instance = mock_service.return_value
        instance.get_relatie.side_effect = VTArchivarisRelatieNotFound('Not found')
        response = client.get('/archivarisrelatie/999')
        assert response.status_code == 404
        assert response.json['message'] == 'Not found'

def test_post_archivarisrelatie_success(client):
    with patch('src.api.vtarchivarisrelatieapi.VTArchivarisRelatieService') as mock_service:
        instance = mock_service.return_value
        instance.create_relatie.return_value = {'id': 42, 'naam': 'Piet', 'archief': '67890'}
        payload = {'naam': 'Piet', 'archief': '67890'}
        response = client.post('/archivarisrelatie', json=payload)
        assert response.status_code == 201
        assert response.json == {'id': 42, 'naam': 'Piet', 'archief': '67890'}
        instance.create_relatie.assert_called_once_with(payload)

def test_post_archivarisrelatie_validation_error(client):
    with patch('src.api.vtarchivarisrelatieapi.VTArchivarisRelatieService') as mock_service:
        instance = mock_service.return_value
        instance.create_relatie.side_effect = VTArchivarisRelatieValidationError('Invalid data.')
        payload = {'naam': '', 'archief': ''}
        response = client.post('/archivarisrelatie', json=payload)
        assert response.status_code == 400
        assert response.json['message'] == 'Invalid data.'

def test_patch_archivarisrelatie_success(client):
    with patch('src.api.vtarchivarisrelatieapi.VTArchivarisRelatieService') as mock_service:
        instance = mock_service.return_value
        instance.update_relatie.return_value = {'id': 4, 'naam': 'Kees', 'archief': 'A-111'}
        payload = {'naam': 'Kees'}
        response = client.patch('/archivarisrelatie/4', json=payload)
        assert response.status_code == 200
        assert response.json == {'id': 4, 'naam': 'Kees', 'archief': 'A-111'}
        instance.update_relatie.assert_called_once_with(4, payload)

def test_patch_archivarisrelatie_not_found(client):
    with patch('src.api.vtarchivarisrelatieapi.VTArchivarisRelatieService') as mock_service:
        instance = mock_service.return_value
        instance.update_relatie.side_effect = VTArchivarisRelatieNotFound("Relatie bestaat niet.")
        payload = {'naam': 'Kees'}
        response = client.patch('/archivarisrelatie/9999', json=payload)
        assert response.status_code == 404
        assert response.json['message'] == 'Relatie bestaat niet.'

def test_delete_archivarisrelatie_success(client):
    with patch('src.api.vtarchivarisrelatieapi.VTArchivarisRelatieService') as mock_service:
        instance = mock_service.return_value
        instance.delete_relatie.return_value = None
        response = client.delete('/archivarisrelatie/6')
        assert response.status_code == 204
        instance.delete_relatie.assert_called_once_with(6)

def test_delete_archivarisrelatie_not_found(client):
    with patch('src.api.vtarchivarisrelatieapi.VTArchivarisRelatieService') as mock_service:
        instance = mock_service.return_value
        instance.delete_relatie.side_effect = VTArchivarisRelatieNotFound("Niet gevonden.")
        response = client.delete('/archivarisrelatie/7')
        assert response.status_code == 404
        assert response.json['message'] == 'Niet gevonden.'