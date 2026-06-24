import pytest
from src.api import vtarchivarisrelatieapi
from src.api.vtarchivarisrelatieapi_exceptions import (
    VTArchivarisRelatieAPINotFound,
    VTArchivarisRelatieAPIInvalidInput
)
from flask import Flask

@pytest.fixture
def api_app():
    vtarchivarisrelatieapi.reset_vtarchivarisrelaties()
    app = vtarchivarisrelatieapi.create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(api_app):
    return api_app.test_client()

@pytest.fixture(autouse=True)
def _cleanup():
    vtarchivarisrelatieapi.reset_vtarchivarisrelaties()
    yield
    vtarchivarisrelatieapi.reset_vtarchivarisrelaties()

def test_create_and_get_vtarchivarisrelatie():
    vtarchivarisrelatieapi.reset_vtarchivarisrelaties()
    data = {"naam": "Test Archivaris"}
    created = vtarchivarisrelatieapi.create_vtarchivarisrelatie(data)
    relatie_id = created["id"]
    fetched = vtarchivarisrelatieapi.get_vtarchivarisrelatie(relatie_id)
    assert fetched["id"] == relatie_id
    assert fetched["naam"] == "Test Archivaris"

def test_get_vtarchivarisrelatie_not_found():
    vtarchivarisrelatieapi.reset_vtarchivarisrelaties()
    with pytest.raises(VTArchivarisRelatieAPINotFound):
        vtarchivarisrelatieapi.get_vtarchivarisrelatie(9999)

def test_create_vtarchivarisrelatie_invalid_input():
    vtarchivarisrelatieapi.reset_vtarchivarisrelaties()
    with pytest.raises(VTArchivarisRelatieAPIInvalidInput):
        vtarchivarisrelatieapi.create_vtarchivarisrelatie({"naam": ""})
    with pytest.raises(VTArchivarisRelatieAPIInvalidInput):
        vtarchivarisrelatieapi.create_vtarchivarisrelatie({})

def test_update_vtarchivarisrelatie_success():
    vtarchivarisrelatieapi.reset_vtarchivarisrelaties()
    data = {"naam": "Oude Naam"}
    created = vtarchivarisrelatieapi.create_vtarchivarisrelatie(data)
    relatie_id = created["id"]
    updated = vtarchivarisrelatieapi.update_vtarchivarisrelatie(relatie_id, {"naam": "Nieuwe Naam"})
    assert updated["id"] == relatie_id
    assert updated["naam"] == "Nieuwe Naam"

def test_update_vtarchivarisrelatie_invalid():
    vtarchivarisrelatieapi.reset_vtarchivarisrelaties()
    data = {"naam": "Test"}
    created = vtarchivarisrelatieapi.create_vtarchivarisrelatie(data)
    relatie_id = created["id"]
    with pytest.raises(VTArchivarisRelatieAPIInvalidInput):
        vtarchivarisrelatieapi.update_vtarchivarisrelatie(relatie_id, {"naam": ""})
    with pytest.raises(VTArchivarisRelatieAPIInvalidInput):
        vtarchivarisrelatieapi.update_vtarchivarisrelatie(relatie_id, {})
    with pytest.raises(VTArchivarisRelatieAPINotFound):
        vtarchivarisrelatieapi.update_vtarchivarisrelatie(99999, {"naam": "X"})

def test_delete_vtarchivarisrelatie_success():
    vtarchivarisrelatieapi.reset_vtarchivarisrelaties()
    data = {"naam": "DelTest"}
    created = vtarchivarisrelatieapi.create_vtarchivarisrelatie(data)
    relatie_id = created["id"]
    vtarchivarisrelatieapi.delete_vtarchivarisrelatie(relatie_id)
    with pytest.raises(VTArchivarisRelatieAPINotFound):
        vtarchivarisrelatieapi.get_vtarchivarisrelatie(relatie_id)

def test_delete_vtarchivarisrelatie_not_found():
    vtarchivarisrelatieapi.reset_vtarchivarisrelaties()
    with pytest.raises(VTArchivarisRelatieAPINotFound):
        vtarchivarisrelatieapi.delete_vtarchivarisrelatie(9999)

def test_rest_create_get_update_delete(client):
    vtarchivarisrelatieapi.reset_vtarchivarisrelaties()
    # Create
    r = client.post("/vtarchivarisrelaties", json={"naam": "API Archivaris"})
    assert r.status_code == 201
    result = r.get_json()
    rid = result["id"]
    assert result["naam"] == "API Archivaris"
    # Get
    r2 = client.get(f"/vtarchivarisrelaties/{rid}")
    assert r2.status_code == 200
    assert r2.get_json()["naam"] == "API Archivaris"
    # Update
    r3 = client.put(f"/vtarchivarisrelaties/{rid}", json={"naam": "Gewijzigd"})
    assert r3.status_code == 200
    assert r3.get_json()["naam"] == "Gewijzigd"
    # Delete
    r4 = client.delete(f"/vtarchivarisrelaties/{rid}")
    assert r4.status_code == 204
    # Get after delete
    r5 = client.get(f"/vtarchivarisrelaties/{rid}")
    assert r5.status_code == 404
