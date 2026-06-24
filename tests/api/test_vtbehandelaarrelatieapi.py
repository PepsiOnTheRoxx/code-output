import pytest
from unittest.mock import patch, MagicMock
from src.api import vtbehandelaarrelatieapi
from src.api import vtbehandelaarrelatieapi_exceptions

@pytest.fixture
def api_client():
    with patch('src.api.vtbehandelaarrelatieapi.SomeAPIClient') as MockClient:
        yield MockClient.return_value

def test_create_vtbehandelaarrelatie_success(api_client):
    relatie_data = {'behandelaar_id': 1, 'vt_case_id': 101}
    api_client.create_relatie.return_value = {'id': 123, 'behandelaar_id': 1, 'vt_case_id': 101}
    with patch('src.api.vtbehandelaarrelatieapi.SomeAPIClient', return_value=api_client):
        result = vtbehandelaarrelatieapi.create_relatie(relatie_data)
        assert result['id'] == 123
        assert result['behandelaar_id'] == 1
        assert result['vt_case_id'] == 101

def test_create_vtbehandelaarrelatie_validation_error(api_client):
    relatie_data = {'behandelaar_id': None, 'vt_case_id': 101}
    api_client.create_relatie.side_effect = vtbehandelaarrelatieapi_exceptions.ValidationException('Invalid data')
    with patch('src.api.vtbehandelaarrelatieapi.SomeAPIClient', return_value=api_client):
        with pytest.raises(vtbehandelaarrelatieapi_exceptions.ValidationException):
            vtbehandelaarrelatieapi.create_relatie(relatie_data)

def test_get_vtbehandelaarrelatie_success(api_client):
    api_client.get_relatie.return_value = {'id': 123, 'behandelaar_id': 1, 'vt_case_id': 101}
    with patch('src.api.vtbehandelaarrelatieapi.SomeAPIClient', return_value=api_client):
        result = vtbehandelaarrelatieapi.get_relatie(123)
        assert result['id'] == 123
        assert result['behandelaar_id'] == 1

def test_get_vtbehandelaarrelatie_not_found(api_client):
    api_client.get_relatie.side_effect = vtbehandelaarrelatieapi_exceptions.NotFoundException('Relatie not found')
    with patch('src.api.vtbehandelaarrelatieapi.SomeAPIClient', return_value=api_client):
        with pytest.raises(vtbehandelaarrelatieapi_exceptions.NotFoundException):
            vtbehandelaarrelatieapi.get_relatie(999)

def test_update_vtbehandelaarrelatie_success(api_client):
    relatie_update = {'behandelaar_id': 2}
    api_client.update_relatie.return_value = {'id': 123, 'behandelaar_id': 2, 'vt_case_id': 101}
    with patch('src.api.vtbehandelaarrelatieapi.SomeAPIClient', return_value=api_client):
        result = vtbehandelaarrelatieapi.update_relatie(123, relatie_update)
        assert result['behandelaar_id'] == 2

def test_update_vtbehandelaarrelatie_not_found(api_client):
    relatie_update = {'behandelaar_id': 2}
    api_client.update_relatie.side_effect = vtbehandelaarrelatieapi_exceptions.NotFoundException('Relatie not found')
    with patch('src.api.vtbehandelaarrelatieapi.SomeAPIClient', return_value=api_client):
        with pytest.raises(vtbehandelaarrelatieapi_exceptions.NotFoundException):
            vtbehandelaarrelatieapi.update_relatie(999, relatie_update)

def test_delete_vtbehandelaarrelatie_success(api_client):
    api_client.delete_relatie.return_value = None
    with patch('src.api.vtbehandelaarrelatieapi.SomeAPIClient', return_value=api_client):
        result = vtbehandelaarrelatieapi.delete_relatie(123)
        assert result is None

def test_delete_vtbehandelaarrelatie_not_found(api_client):
    api_client.delete_relatie.side_effect = vtbehandelaarrelatieapi_exceptions.NotFoundException('Relatie not found')
    with patch('src.api.vtbehandelaarrelatieapi.SomeAPIClient', return_value=api_client):
        with pytest.raises(vtbehandelaarrelatieapi_exceptions.NotFoundException):
            vtbehandelaarrelatieapi.delete_relatie(999)
