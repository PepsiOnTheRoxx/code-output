import pytest
from unittest.mock import patch, MagicMock
from src.api import vtarchivarisrelatieapi
from src.api import vtarchivarisrelatieapi_exceptions

def test_get_vtarchivarisrelatie_success():
    with patch("src.api.vtarchivarisrelatieapi.get_vtarchivarisrelatie") as mock_get:
        mock_get.return_value = {"id": 1, "naam": "Test Archivaris"}
        response = vtarchivarisrelatieapi.get_vtarchivarisrelatie(1)
        assert response["id"] == 1
        assert response["naam"] == "Test Archivaris"

def test_get_vtarchivarisrelatie_not_found():
    with patch("src.api.vtarchivarisrelatieapi.get_vtarchivarisrelatie") as mock_get:
        mock_get.side_effect = vtarchivarisrelatieapi_exceptions.VTArchivarisRelatieAPINotFound()
        with pytest.raises(vtarchivarisrelatieapi_exceptions.VTArchivarisRelatieAPINotFound):
            vtarchivarisrelatieapi.get_vtarchivarisrelatie(99)

def test_create_vtarchivarisrelatie_success():
    data = {"naam": "Nieuwe Archivaris"}
    with patch("src.api.vtarchivarisrelatieapi.create_vtarchivarisrelatie") as mock_create:
        mock_create.return_value = {"id": 2, "naam": "Nieuwe Archivaris"}
        response = vtarchivarisrelatieapi.create_vtarchivarisrelatie(data)
        assert response["id"] == 2
        assert response["naam"] == "Nieuwe Archivaris"

def test_create_vtarchivarisrelatie_invalid_input():
    data = {"naam": ""}
    with patch("src.api.vtarchivarisrelatieapi.create_vtarchivarisrelatie") as mock_create:
        mock_create.side_effect = vtarchivarisrelatieapi_exceptions.VTArchivarisRelatieAPIInvalidInput()
        with pytest.raises(vtarchivarisrelatieapi_exceptions.VTArchivarisRelatieAPIInvalidInput):
            vtarchivarisrelatieapi.create_vtarchivarisrelatie(data)

def test_update_vtarchivarisrelatie_success():
    data = {"naam": "Aangepaste Archivaris"}
    with patch("src.api.vtarchivarisrelatieapi.update_vtarchivarisrelatie") as mock_update:
        mock_update.return_value = {"id": 1, "naam": "Aangepaste Archivaris"}
        response = vtarchivarisrelatieapi.update_vtarchivarisrelatie(1, data)
        assert response["id"] == 1
        assert response["naam"] == "Aangepaste Archivaris"

def test_update_vtarchivarisrelatie_not_found():
    data = {"naam": "Onbekend"}
    with patch("src.api.vtarchivarisrelatieapi.update_vtarchivarisrelatie") as mock_update:
        mock_update.side_effect = vtarchivarisrelatieapi_exceptions.VTArchivarisRelatieAPINotFound()
        with pytest.raises(vtarchivarisrelatieapi_exceptions.VTArchivarisRelatieAPINotFound):
            vtarchivarisrelatieapi.update_vtarchivarisrelatie(99, data)

def test_delete_vtarchivarisrelatie_success():
    with patch("src.api.vtarchivarisrelatieapi.delete_vtarchivarisrelatie") as mock_delete:
        mock_delete.return_value = None
        result = vtarchivarisrelatieapi.delete_vtarchivarisrelatie(1)
        assert result is None

def test_delete_vtarchivarisrelatie_not_found():
    with patch("src.api.vtarchivarisrelatieapi.delete_vtarchivarisrelatie") as mock_delete:
        mock_delete.side_effect = vtarchivarisrelatieapi_exceptions.VTArchivarisRelatieAPINotFound()
        with pytest.raises(vtarchivarisrelatieapi_exceptions.VTArchivarisRelatieAPINotFound):
            vtarchivarisrelatieapi.delete_vtarchivarisrelatie(99)
