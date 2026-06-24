import pytest
from unittest.mock import patch, MagicMock
from src.api import vtproceseigenaarrelatieapi
from src.api import vtproceseigenaarrelatieapi_exceptions

@pytest.fixture
def client():
    with patch('src.api.vtproceseigenaarrelatieapi.app.test_client') as test_client:
        yield test_client.return_value

def test_get_proceseigenaarrelatie_success(client):
    mock_response = {'id': 1, 'proceseigenaar_id': 123, 'proces_id': 456}
    with patch('src.api.vtproceseigenaarrelatieapi.get_proceseigenaarrelatie_by_id', return_value=mock_response):
        response = client.get('/vt/proceseigenaarrelatie/1')
        assert response.status_code == 200
        assert response.get_json() == mock_response

def test_get_proceseigenaarrelatie_not_found(client):
    with patch('src.api.vtproceseigenaarrelatieapi.get_proceseigenaarrelatie_by_id', side_effect=vtproceseigenaarrelatieapi_exceptions.ProceseigenaarRelatieNotFoundError):
        response = client.get('/vt/proceseigenaarrelatie/999')
        assert response.status_code == 404

def test_post_proceseigenaarrelatie_success(client):
    req_data = {'proceseigenaar_id': 123, 'proces_id': 456}
    mock_obj = {'id': 2, 'proceseigenaar_id': 123, 'proces_id': 456}
    with patch('src.api.vtproceseigenaarrelatieapi.create_proceseigenaarrelatie', return_value=mock_obj):
        response = client.post('/vt/proceseigenaarrelatie', json=req_data)
        assert response.status_code == 201
        assert response.get_json() == mock_obj

def test_post_proceseigenaarrelatie_invalid_data(client):
    with patch('src.api.vtproceseigenaarrelatieapi.create_proceseigenaarrelatie', side_effect=vtproceseigenaarrelatieapi_exceptions.InvalidProceseigenaarRelatieData):
        response = client.post('/vt/proceseigenaarrelatie', json={})
        assert response.status_code == 400

def test_delete_proceseigenaarrelatie_success(client):
    with patch('src.api.vtproceseigenaarrelatieapi.delete_proceseigenaarrelatie', return_value=None):
        response = client.delete('/vt/proceseigenaarrelatie/1')
        assert response.status_code == 204

def test_delete_proceseigenaarrelatie_not_found(client):
    with patch('src.api.vtproceseigenaarrelatieapi.delete_proceseigenaarrelatie', side_effect=vtproceseigenaarrelatieapi_exceptions.ProceseigenaarRelatieNotFoundError):
        response = client.delete('/vt/proceseigenaarrelatie/999')
        assert response.status_code == 404

def test_list_proceseigenaarrelaties_success(client):
    mock_list = [
        {'id': 1, 'proceseigenaar_id': 123, 'proces_id': 456},
        {'id': 2, 'proceseigenaar_id': 124, 'proces_id': 457}
    ]
    with patch('src.api.vtproceseigenaarrelatieapi.list_proceseigenaarrelaties', return_value=mock_list):
        response = client.get('/vt/proceseigenaarrelatie')
        assert response.status_code == 200
        assert response.get_json() == mock_list