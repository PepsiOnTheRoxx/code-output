import pytest
from unittest.mock import patch, MagicMock
from src.api.vtarchivarisrelatieapi import VTArchivarisRelatieAPI
from src.api.vtarchivarisrelatieapi_exceptions import VTArchivarisRelatieNotFound, VTArchivarisRelatieValidationError

@pytest.fixture
def client():
    # Patch VTArchivarisRelatieService before instantiating the API
    with patch('src.api.vtarchivarisrelatieapi.VTArchivarisRelatieService') as mock_service_cls:
        mock_service = mock_service_cls.return_value
        app = VTArchivarisRelatieAPI().app
        app.config['TESTING'] = True
        with app.test_client() as client:
            # Attach mock to client so tests can access
            client.mock_service = mock_service
            yield client

def test_get_archivarisrelatie_success(client):
    client.mock_service.get_relatie.return_value = {'id': 1, 'naam': 'Jan', 'archief': '12345'}
    response = client.get('/archivarisrelatie/1')
    assert response.status_code == 200
    assert response.json == {'id': 1, 'naam': 'Jan', 'archief': '12345'}
    client.mock_service.get_relatie.assert_called_once_with(1)

def test_get_archivarisrelatie_not_found(client):
    client.mock_service.get_relatie.side_effect = VTArchivarisRelatieNotFound('Not found')
    response = client.get('/archivarisrelatie/999')
    assert response.status_code == 404
    assert response.json['message'] == 'Not found'

def test_post_archivarisrelatie_success(client):
    client.mock_service.create_relatie.return_value = {'id': 42, 'naam': 'Piet', 'archief': '67890'}
    payload = {'naam': 'Piet', 'archief': '67890'}
    response = client.post('/archivarisrelatie', json=payload)
    assert response.status_code == 201
    assert response.json == {'id': 42, 'naam': 'Piet', 'archief': '67890'}
    client.mock_service.create_relatie.assert_called_once_with(payload)

def test_post_archivarisrelatie_validation_error(client):
    client.mock_service.create_relatie.side_effect = VTArchivarisRelatieValidationError('Invalid data.')
    payload = {'naam': '', 'archief': ''}
    response = client.post('/archivarisrelatie', json=payload)
    assert response.status_code == 400
    assert response.json['message'] == 'Invalid data.'

def test_patch_archivarisrelatie_success(client):
    client.mock_service.update_relatie.return_value = {'id': 4, 'naam': 'Kees', 'archief': 'A-111'}
    payload = {'naam': 'Kees'}
    response = client.patch('/archivarisrelatie/4', json=payload)
    assert response.status_code == 200
    assert response.json == {'id': 4, 'naam': 'Kees', 'archief': 'A-111'}
    client.mock_service.update_relatie.assert_called_once_with(4, payload)

def test_patch_archivarisrelatie_not_found(client):
    client.mock_service.update_relatie.side_effect = VTArchivarisRelatieNotFound("Relatie bestaat niet.")
    payload = {'naam': 'Kees'}
    response = client.patch('/archivarisrelatie/9999', json=payload)
    assert response.status_code == 404
    assert response.json['message'] == 'Relatie bestaat niet.'

def test_delete_archivarisrelatie_success(client):
    client.mock_service.delete_relatie.return_value = None
    response = client.delete('/archivarisrelatie/6')
    assert response.status_code == 204
    client.mock_service.delete_relatie.assert_called_once_with(6)

def test_delete_archivarisrelatie_not_found(client):
    client.mock_service.delete_relatie.side_effect = VTArchivarisRelatieNotFound("Niet gevonden.")
    response = client.delete('/archivarisrelatie/7')
    assert response.status_code == 404
    assert response.json['message'] == 'Niet gevonden.'
