import pytest
from src.services.managevtarchivarisrelatie import VTArchivarisRelatieService, USERS, TAKEN, User, Taak, ARCHIVARIS_RELATIES
from src.services.managevtarchivarisrelatie_exceptions import (
    ArchivarisAlreadyExistsException,
    ArchivarisRelationNotFoundException,
    UserNotFoundException,
    VernietigingstaakNotFoundException
)

def setup_module(module):
    USERS.clear()
    TAKEN.clear()
    ARCHIVARIS_RELATIES.clear()
    USERS[100] = User(100)
    USERS[101] = User(101)
    USERS[103] = User(103)
    USERS[104] = User(104)
    USERS[105] = User(105)
    USERS[1] = User(1)
    USERS[2] = User(2)
    USERS[120] = User(120)
    USERS[121] = User(121)
    TAKEN[200] = Taak(200)
    TAKEN[201] = Taak(201)
    TAKEN[202] = Taak(202)
    TAKEN[203] = Taak(203)
    TAKEN[204] = Taak(204)
    TAKEN[205] = Taak(205)
    TAKEN[206] = Taak(206)
    TAKEN[220] = Taak(220)
    TAKEN[221] = Taak(221)

def test_add_archivaris_success():
    service = VTArchivarisRelatieService()
    user_id = 100
    taak_id = 200
    service.add_archivaris(user_id, taak_id)
    assert (user_id, taak_id) in service.ARCHIVARIS_RELATIES or (user_id, taak_id) in ARCHIVARIS_RELATIES

def test_add_archivaris_user_not_found():
    service = VTArchivarisRelatieService()
    user_id = 999999
    taak_id = 201
    with pytest.raises(UserNotFoundException):
        service.add_archivaris(user_id, taak_id)

def test_add_archivaris_taak_not_found():
    service = VTArchivarisRelatieService()
    user_id = 101
    taak_id = 999999
    with pytest.raises(VernietigingstaakNotFoundException):
        service.add_archivaris(user_id, taak_id)

def test_add_archivaris_already_exists():
    service = VTArchivarisRelatieService()
    user_id = 103
    taak_id = 203
    service.add_archivaris(user_id, taak_id)
    with pytest.raises(ArchivarisAlreadyExistsException):
        service.add_archivaris(user_id, taak_id)

def test_remove_archivaris_success():
    service = VTArchivarisRelatieService()
    user_id = 104
    taak_id = 204
    service.add_archivaris(user_id, taak_id)
    service.remove_archivaris(user_id, taak_id)
    assert (user_id, taak_id) not in ARCHIVARIS_RELATIES

def test_remove_archivaris_not_found():
    service = VTArchivarisRelatieService()
    user_id = 105
    taak_id = 205
    with pytest.raises(ArchivarisRelationNotFoundException):
        service.remove_archivaris(user_id, taak_id)

def test_get_archivarissen_for_taak_returns_list():
    service = VTArchivarisRelatieService()
    taak_id = 206
    service.add_archivaris(1, taak_id)
    service.add_archivaris(2, taak_id)
    result = service.get_archivarissen_for_taak(taak_id)
    ids = [user.id for user in result]
    assert sorted(ids) == [1, 2]

def test_get_archivarissen_for_taak_taak_not_found():
    service = VTArchivarisRelatieService()
    taak_id = 999
    with pytest.raises(VernietigingstaakNotFoundException):
        service.get_archivarissen_for_taak(taak_id)

def test_is_user_archivaris_of_taak_true():
    service = VTArchivarisRelatieService()
    user_id = 120
    taak_id = 220
    service.add_archivaris(user_id, taak_id)
    assert service.is_user_archivaris_of_taak(user_id, taak_id) is True

def test_is_user_archivaris_of_taak_false():
    service = VTArchivarisRelatieService()
    user_id = 121
    taak_id = 221
    assert service.is_user_archivaris_of_taak(user_id, taak_id) is False
