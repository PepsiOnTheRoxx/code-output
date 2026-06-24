import pytest
from unittest.mock import patch, MagicMock
from src.services.updatebron import update_bron
from src.services.updatebron_exceptions import BronNotFoundException, InvalidBronDataException


def test_update_bron_success():
    bron_id = 12
    new_data = {"naam": "Nieuwe Bron"}
    old_bron = {"id": bron_id, "naam": "Oude Bron"}
    updated_bron = {"id": bron_id, "naam": "Nieuwe Bron"}

    with patch("src.services.updatebron.get_bron_by_id") as mock_get, \
         patch("src.services.updatebron.save_bron") as mock_save:
        mock_get.return_value = old_bron
        mock_save.return_value = updated_bron

        result = update_bron(bron_id, new_data)

        mock_get.assert_called_once_with(bron_id)
        mock_save.assert_called_once_with(updated_bron)
        assert result == updated_bron

def test_update_bron_raises_not_found():
    bron_id = 99
    new_data = {"naam": "Niet Bestaande Bron"}

    with patch("src.services.updatebron.get_bron_by_id") as mock_get:
        mock_get.return_value = None

        with pytest.raises(BronNotFoundException):
            update_bron(bron_id, new_data)

def test_update_bron_raises_invalid_data():
    bron_id = 12
    new_data = {"naam": ""}  # Stel lege naam is ongeldig
    old_bron = {"id": bron_id, "naam": "Oude Bron"}

    with patch("src.services.updatebron.get_bron_by_id") as mock_get, \
         patch("src.services.updatebron.validate_bron_data") as mock_validate:
        mock_get.return_value = old_bron
        mock_validate.side_effect = InvalidBronDataException()

        with pytest.raises(InvalidBronDataException):
            update_bron(bron_id, new_data)

def test_update_bron_partial_update():
    bron_id = 12
    new_data = {"beschrijving": "Aangepaste beschrijving"}
    old_bron = {"id": bron_id, "naam": "Bron", "beschrijving": "Oud"}
    updated_bron = {"id": bron_id, "naam": "Bron", "beschrijving": "Aangepaste beschrijving"}

    with patch("src.services.updatebron.get_bron_by_id") as mock_get, \
         patch("src.services.updatebron.save_bron") as mock_save:
        mock_get.return_value = old_bron
        mock_save.return_value = updated_bron

        result = update_bron(bron_id, new_data)

        mock_get.assert_called_once_with(bron_id)
        mock_save.assert_called_once()
        assert result == updated_bron

def test_update_bron_calls_validation():
    bron_id = 12
    new_data = {"naam": "BronX"}
    old_bron = {"id": bron_id, "naam": "Bron"}

    with patch("src.services.updatebron.get_bron_by_id") as mock_get, \
         patch("src.services.updatebron.save_bron") as mock_save, \
         patch("src.services.updatebron.validate_bron_data") as mock_validate:
        mock_get.return_value = old_bron
        mock_validate.return_value = None
        mock_save.return_value = {"id": bron_id, "naam": "BronX"}

        result = update_bron(bron_id, new_data)

        mock_validate.assert_called_once_with({"id": bron_id, "naam": "BronX"})
        assert result["naam"] == "BronX"
