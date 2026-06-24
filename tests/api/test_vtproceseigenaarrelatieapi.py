import pytest
from unittest.mock import patch, MagicMock
from src.api.vtproceseigenaarrelatieapi import (
    get_relatie,
    create_relatie,
    update_relatie,
    delete_relatie,
    list_relaties,
)
from src.api.vtproceseigenaarrelatieapi_exceptions import (
    RelatieNotFoundException,
    RelatieAlreadyExistsException,
    InvalidRelatieDataException,
)

def test_get_relatie_returns_data():
    expected = {"id": 1, "proceseigenaar_id": 10, "facttype_id": 5}
    with patch("src.api.vtproceseigenaarrelatieapi.get_relatie", return_value=expected) as mock_get:
        result = get_relatie(1)
        assert result == expected
        mock_get.assert_called_once_with(1)

def test_get_relatie_not_found():
    with patch("src.api.vtproceseigenaarrelatieapi.get_relatie", side_effect=RelatieNotFoundException):
        with pytest.raises(RelatieNotFoundException):
            get_relatie(999)

def test_create_relatie_succeeds():
    relatie_data = {"proceseigenaar_id": 12, "facttype_id": 5}
    expected = {"id": 2, **relatie_data}
    with patch("src.api.vtproceseigenaarrelatieapi.create_relatie", return_value=expected) as mock_create:
        result = create_relatie(relatie_data)
        assert result == expected
        mock_create.assert_called_once_with(relatie_data)

def test_create_relatie_already_exists():
    relatie_data = {"proceseigenaar_id": 12, "facttype_id": 5}
    with patch("src.api.vtproceseigenaarrelatieapi.create_relatie", side_effect=RelatieAlreadyExistsException):
        with pytest.raises(RelatieAlreadyExistsException):
            create_relatie(relatie_data)

def test_create_relatie_invalid_data():
    relatie_data = {"proceseigenaar_id": None, "facttype_id": 5}
    with patch("src.api.vtproceseigenaarrelatieapi.create_relatie", side_effect=InvalidRelatieDataException):
        with pytest.raises(InvalidRelatieDataException):
            create_relatie(relatie_data)

def test_update_relatie_success():
    relatie_id = 1
    update_data = {"proceseigenaar_id": 14}
    expected = {"id": 1, "proceseigenaar_id": 14, "facttype_id": 5}
    with patch("src.api.vtproceseigenaarrelatieapi.update_relatie", return_value=expected) as mock_update:
        result = update_relatie(relatie_id, update_data)
        assert result == expected
        mock_update.assert_called_once_with(relatie_id, update_data)

def test_update_relatie_not_found():
    relatie_id = 999
    update_data = {"proceseigenaar_id": 15}
    with patch("src.api.vtproceseigenaarrelatieapi.update_relatie", side_effect=RelatieNotFoundException):
        with pytest.raises(RelatieNotFoundException):
            update_relatie(relatie_id, update_data)

def test_update_relatie_invalid_data():
    relatie_id = 1
    update_data = {"proceseigenaar_id": None}
    with patch("src.api.vtproceseigenaarrelatieapi.update_relatie", side_effect=InvalidRelatieDataException):
        with pytest.raises(InvalidRelatieDataException):
            update_relatie(relatie_id, update_data)

def test_delete_relatie_success():
    with patch("src.api.vtproceseigenaarrelatieapi.delete_relatie", return_value=None) as mock_delete:
        assert delete_relatie(1) is None
        mock_delete.assert_called_once_with(1)

def test_delete_relatie_not_found():
    with patch("src.api.vtproceseigenaarrelatieapi.delete_relatie", side_effect=RelatieNotFoundException):
        with pytest.raises(RelatieNotFoundException):
            delete_relatie(100)

def test_list_relaties_returns_list():
    expected = [
        {"id": 1, "proceseigenaar_id": 11, "facttype_id": 5},
        {"id": 2, "proceseigenaar_id": 12, "facttype_id": 5},
    ]
    with patch("src.api.vtproceseigenaarrelatieapi.list_relaties", return_value=expected) as mock_list:
        result = list_relaties()
        assert result == expected
        mock_list.assert_called_once_with()

def test_list_relaties_empty():
    with patch("src.api.vtproceseigenaarrelatieapi.list_relaties", return_value=[]) as mock_list:
        result = list_relaties()
        assert result == []
        mock_list.assert_called_once_with()