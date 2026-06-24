import pytest
from unittest.mock import patch, MagicMock
from src.api.vtbronnenrelatieapi_exceptions import (
    VTBronnenRelatieNotFound,
    VTBronnenRelatieAlreadyExists,
    VTBronnenRelatieInvalidData,
    VTBronnenRelatieDatabaseError
)
from src.api import vtbronnenrelatieapi

def test_get_relatie_success():
    expected_result = {"id": 1, "bron": "A", "relatie": "B"}
    with patch("src.api.vtbronnenrelatieapi.get_relatie", return_value=expected_result) as mock_func:
        result = vtbronnenrelatieapi.get_relatie(1)
        assert result == expected_result
        mock_func.assert_called_once_with(1)

def test_get_relatie_not_found():
    with patch("src.api.vtbronnenrelatieapi.get_relatie", side_effect=VTBronnenRelatieNotFound):
        with pytest.raises(VTBronnenRelatieNotFound):
            vtbronnenrelatieapi.get_relatie(999)

def test_create_relatie_success():
    input_data = {"bron": "A", "relatie": "B"}
    expected_result = {"id": 2, **input_data}
    with patch("src.api.vtbronnenrelatieapi.create_relatie", return_value=expected_result) as mock_func:
        result = vtbronnenrelatieapi.create_relatie(input_data)
        assert result == expected_result
        mock_func.assert_called_once_with(input_data)

def test_create_relatie_already_exists():
    input_data = {"bron": "A", "relatie": "B"}
    with patch("src.api.vtbronnenrelatieapi.create_relatie", side_effect=VTBronnenRelatieAlreadyExists):
        with pytest.raises(VTBronnenRelatieAlreadyExists):
            vtbronnenrelatieapi.create_relatie(input_data)

def test_create_relatie_invalid_data():
    input_data = {"bron": "", "relatie": "B"}
    with patch("src.api.vtbronnenrelatieapi.create_relatie", side_effect=VTBronnenRelatieInvalidData):
        with pytest.raises(VTBronnenRelatieInvalidData):
            vtbronnenrelatieapi.create_relatie(input_data)

def test_update_relatie_success():
    update_data = {"relatie": "C"}
    expected_result = {"id": 1, "bron": "A", "relatie": "C"}
    with patch("src.api.vtbronnenrelatieapi.update_relatie", return_value=expected_result) as mock_func:
        result = vtbronnenrelatieapi.update_relatie(1, update_data)
        assert result == expected_result
        mock_func.assert_called_once_with(1, update_data)

def test_update_relatie_not_found():
    update_data = {"relatie": "C"}
    with patch("src.api.vtbronnenrelatieapi.update_relatie", side_effect=VTBronnenRelatieNotFound):
        with pytest.raises(VTBronnenRelatieNotFound):
            vtbronnenrelatieapi.update_relatie(777, update_data)

def test_update_relatie_invalid_data():
    update_data = {"relatie": ""}
    with patch("src.api.vtbronnenrelatieapi.update_relatie", side_effect=VTBronnenRelatieInvalidData):
        with pytest.raises(VTBronnenRelatieInvalidData):
            vtbronnenrelatieapi.update_relatie(1, update_data)

def test_delete_relatie_success():
    with patch("src.api.vtbronnenrelatieapi.delete_relatie", return_value=None) as mock_func:
        result = vtbronnenrelatieapi.delete_relatie(1)
        assert result is None
        mock_func.assert_called_once_with(1)

def test_delete_relatie_not_found():
    with patch("src.api.vtbronnenrelatieapi.delete_relatie", side_effect=VTBronnenRelatieNotFound):
        with pytest.raises(VTBronnenRelatieNotFound):
            vtbronnenrelatieapi.delete_relatie(999)

def test_get_all_success():
    expected = [
        {"id": 1, "bron": "A", "relatie": "B"},
        {"id": 2, "bron": "D", "relatie": "E"}
    ]
    with patch("src.api.vtbronnenrelatieapi.get_all_relaties", return_value=expected) as mock_func:
        result = vtbronnenrelatieapi.get_all_relaties()
        assert result == expected
        mock_func.assert_called_once_with()

def test_database_error_on_get():
    with patch("src.api.vtbronnenrelatieapi.get_relatie", side_effect=VTBronnenRelatieDatabaseError):
        with pytest.raises(VTBronnenRelatieDatabaseError):
            vtbronnenrelatieapi.get_relatie(1)
