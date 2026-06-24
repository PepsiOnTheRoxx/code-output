import pytest
from unittest.mock import patch, MagicMock
from src.services.managevtarchivarisrelatie import VTArchivarisRelatieService
from src.services.managevtarchivarisrelatie_exceptions import (
    ArchivarisAlreadyExistsException,
    ArchivarisRelationNotFoundException,
    UserNotFoundException,
    VernietigingstaakNotFoundException
)


def test_add_archivaris_success():
    service = VTArchivarisRelatieService()
    user_id = 100
    taak_id = 200
    with patch.object(service, "get_user_by_id", return_value=MagicMock(id=user_id)) as mock_user, \
         patch.object(service, "get_vernietigingstaak_by_id", return_value=MagicMock(id=taak_id)) as mock_taak, \
         patch.object(service, "is_user_archivaris_of_taak", return_value=False) as mock_check, \
         patch.object(service, "add_archivaris_relation") as mock_add:
        service.add_archivaris(user_id, taak_id)
        mock_user.assert_called_once_with(user_id)
        mock_taak.assert_called_once_with(taak_id)
        mock_check.assert_called_once_with(user_id, taak_id)
        mock_add.assert_called_once_with(user_id, taak_id)


def test_add_archivaris_user_not_found():
    service = VTArchivarisRelatieService()
    user_id = 101
    taak_id = 201
    with patch.object(service, "get_user_by_id", side_effect=UserNotFoundException):
        with pytest.raises(UserNotFoundException):
            service.add_archivaris(user_id, taak_id)


def test_add_archivaris_taak_not_found():
    service = VTArchivarisRelatieService()
    user_id = 101
    taak_id = 202
    with patch.object(service, "get_user_by_id", return_value=MagicMock()), \
         patch.object(service, "get_vernietigingstaak_by_id", side_effect=VernietigingstaakNotFoundException):
        with pytest.raises(VernietigingstaakNotFoundException):
            service.add_archivaris(user_id, taak_id)


def test_add_archivaris_already_exists():
    service = VTArchivarisRelatieService()
    user_id = 103
    taak_id = 203
    with patch.object(service, "get_user_by_id", return_value=MagicMock()), \
         patch.object(service, "get_vernietigingstaak_by_id", return_value=MagicMock()), \
         patch.object(service, "is_user_archivaris_of_taak", return_value=True):
        with pytest.raises(ArchivarisAlreadyExistsException):
            service.add_archivaris(user_id, taak_id)


def test_remove_archivaris_success():
    service = VTArchivarisRelatieService()
    user_id = 104
    taak_id = 204
    with patch.object(service, "is_user_archivaris_of_taak", return_value=True) as mock_check, \
         patch.object(service, "remove_archivaris_relation") as mock_remove:
        service.remove_archivaris(user_id, taak_id)
        mock_check.assert_called_once_with(user_id, taak_id)
        mock_remove.assert_called_once_with(user_id, taak_id)


def test_remove_archivaris_not_found():
    service = VTArchivarisRelatieService()
    user_id = 105
    taak_id = 205
    with patch.object(service, "is_user_archivaris_of_taak", return_value=False):
        with pytest.raises(ArchivarisRelationNotFoundException):
            service.remove_archivaris(user_id, taak_id)


def test_get_archivarissen_for_taak_returns_list():
    service = VTArchivarisRelatieService()
    taak_id = 206
    users = [MagicMock(id=1), MagicMock(id=2)]
    with patch.object(service, "get_archivarissen_by_taak_id", return_value=users):
        result = service.get_archivarissen_for_taak(taak_id)
        assert result == users


def test_get_archivarissen_for_taak_taak_not_found():
    service = VTArchivarisRelatieService()
    taak_id = 999
    with patch.object(service, "get_vernietigingstaak_by_id", side_effect=VernietigingstaakNotFoundException):
        with pytest.raises(VernietigingstaakNotFoundException):
            service.get_archivarissen_for_taak(taak_id)


def test_is_user_archivaris_of_taak_true():
    service = VTArchivarisRelatieService()
    user_id = 120
    taak_id = 220
    with patch.object(service, "is_user_archivaris_of_taak", return_value=True):
        assert service.is_user_archivaris_of_taak(user_id, taak_id) is True


def test_is_user_archivaris_of_taak_false():
    service = VTArchivarisRelatieService()
    user_id = 121
    taak_id = 221
    with patch.object(service, "is_user_archivaris_of_taak", return_value=False):
        assert service.is_user_archivaris_of_taak(user_id, taak_id) is False