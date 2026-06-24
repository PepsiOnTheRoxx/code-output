import pytest
from src.api.vtproceseigenaarrelatieapi import (
    get_relatie,
    create_relatie,
    update_relatie,
    delete_relatie,
    list_relaties,
    _reset_storage,
)
from src.api.vtproceseigenaarrelatieapi_exceptions import (
    RelatieNotFoundException,
    RelatieAlreadyExistsException,
    InvalidRelatieDataException,
)

@pytest.fixture(autouse=True)
def reset():
    _reset_storage()


def test_get_relatie_returns_data():
    data = {"proceseigenaar_id": 10, "facttype_id": 5}
    resultaat = create_relatie(data)
    assert resultaat["id"] == 1
    fetched = get_relatie(resultaat["id"])
    assert fetched == resultaat


def test_get_relatie_not_found():
    with pytest.raises(RelatieNotFoundException):
        get_relatie(999)


def test_create_relatie_succeeds():
    eerste = create_relatie({"proceseigenaar_id": 11, "facttype_id": 5})
    tweede = create_relatie({"proceseigenaar_id": 12, "facttype_id": 5})
    assert tweede == {"id": 2, "proceseigenaar_id": 12, "facttype_id": 5}
    assert eerste != tweede


def test_create_relatie_already_exists():
    create_relatie({"proceseigenaar_id": 12, "facttype_id": 5})
    with pytest.raises(RelatieAlreadyExistsException):
        create_relatie({"proceseigenaar_id": 12, "facttype_id": 5})


def test_create_relatie_invalid_data():
    with pytest.raises(InvalidRelatieDataException):
        create_relatie({"proceseigenaar_id": None, "facttype_id": 5})
    with pytest.raises(InvalidRelatieDataException):
        create_relatie({"facttype_id": 4})


def test_update_relatie_success():
    eerste = create_relatie({"proceseigenaar_id": 13, "facttype_id": 5})
    update = update_relatie(eerste["id"], {"proceseigenaar_id": 14})
    assert update["id"] == eerste["id"]
    assert update["proceseigenaar_id"] == 14
    assert update["facttype_id"] == 5


def test_update_relatie_not_found():
    with pytest.raises(RelatieNotFoundException):
        update_relatie(999, {"proceseigenaar_id": 14})


def test_update_relatie_invalid_data():
    eerste = create_relatie({"proceseigenaar_id": 13, "facttype_id": 5})
    with pytest.raises(InvalidRelatieDataException):
        update_relatie(eerste["id"], {"proceseigenaar_id": None})


def test_delete_relatie_success():
    eerste = create_relatie({"proceseigenaar_id": 13, "facttype_id": 5})
    assert get_relatie(eerste["id"]) is not None
    delete_relatie(eerste["id"])
    with pytest.raises(RelatieNotFoundException):
        get_relatie(eerste["id"])


def test_delete_relatie_not_found():
    with pytest.raises(RelatieNotFoundException):
        delete_relatie(100)


def test_list_relaties_returns_list():
    eerste = create_relatie({"proceseigenaar_id": 11, "facttype_id": 5})
    tweede = create_relatie({"proceseigenaar_id": 12, "facttype_id": 5})
    relaties = list_relaties()
    assert relaties == [eerste, tweede]


def test_list_relaties_empty():
    assert list_relaties() == []
