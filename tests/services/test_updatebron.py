import pytest
from unittest.mock import patch
from src.services.updatebron import update_bron, db
from src.services.updatebron_exceptions import BronNotFoundException, InvalidBronDataException

def setup_function():
    db.clear()

def test_update_bron_success():
    bron_id = 12
    new_data = {"naam": "Nieuwe Bron"}
    old_bron = {"id": bron_id, "naam": "Oude Bron"}
    updated_bron = {"id": bron_id, "naam": "Nieuwe Bron"}
    db[bron_id] = old_bron.copy()
    result = update_bron(bron_id, new_data)
    assert db[bron_id] == updated_bron
    assert result == updated_bron

def test_update_bron_raises_not_found():
    bron_id = 99
    new_data = {"naam": "Niet Bestaande Bron"}
    if bron_id in db:
        del db[bron_id]
    with pytest.raises(BronNotFoundException):
        update_bron(bron_id, new_data)

def test_update_bron_raises_invalid_data():
    bron_id = 12
    new_data = {"naam": ""}  # Lege naam ongeldig
    old_bron = {"id": bron_id, "naam": "Oude Bron"}
    db[bron_id] = old_bron.copy()
    with pytest.raises(InvalidBronDataException):
        update_bron(bron_id, new_data)

def test_update_bron_partial_update():
    bron_id = 12
    new_data = {"beschrijving": "Aangepaste beschrijving"}
    old_bron = {"id": bron_id, "naam": "Bron", "beschrijving": "Oud"}
    updated_bron = {"id": bron_id, "naam": "Bron", "beschrijving": "Aangepaste beschrijving"}
    db[bron_id] = old_bron.copy()
    result = update_bron(bron_id, new_data)
    assert db[bron_id] == updated_bron
    assert result == updated_bron

def test_update_bron_calls_validation():
    bron_id = 12
    new_data = {"naam": "BronX"}
    old_bron = {"id": bron_id, "naam": "Bron"}
    db[bron_id] = old_bron.copy()
    result = update_bron(bron_id, new_data)
    assert result["naam"] == "BronX"
    assert db[bron_id]["naam"] == "BronX"
