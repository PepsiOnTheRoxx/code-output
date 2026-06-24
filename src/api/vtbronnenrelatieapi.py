from src.api.vtbronnenrelatieapi_exceptions import (
    VTBronnenRelatieNotFound,
    VTBronnenRelatieAlreadyExists,
    VTBronnenRelatieInvalidData,
    VTBronnenRelatieDatabaseError
)

_relatie_storage = {}
_id_counter = [1]

def get_relatie(relatie_id):
    try:
        if relatie_id not in _relatie_storage:
            raise VTBronnenRelatieNotFound()
        return _relatie_storage[relatie_id].copy()
    except VTBronnenRelatieNotFound:
        raise
    except Exception:
        raise VTBronnenRelatieDatabaseError()

def create_relatie(data):
    try:
        if not isinstance(data, dict):
            raise VTBronnenRelatieInvalidData()
        bron = data.get("bron")
        relatie = data.get("relatie")
        if not bron or not relatie:
            raise VTBronnenRelatieInvalidData()
        for item in _relatie_storage.values():
            if item["bron"] == bron and item["relatie"] == relatie:
                raise VTBronnenRelatieAlreadyExists()
        new_id = _id_counter[0]
        _id_counter[0] += 1
        _relatie_storage[new_id] = {"id": new_id, "bron": bron, "relatie": relatie}
        return _relatie_storage[new_id].copy()
    except (VTBronnenRelatieInvalidData, VTBronnenRelatieAlreadyExists):
        raise
    except Exception:
        raise VTBronnenRelatieDatabaseError()

def update_relatie(relatie_id, data):
    try:
        if relatie_id not in _relatie_storage:
            raise VTBronnenRelatieNotFound()
        if not isinstance(data, dict):
            raise VTBronnenRelatieInvalidData()
        if "relatie" in data and not data["relatie"]:
            raise VTBronnenRelatieInvalidData()
        _relatie_storage[relatie_id].update(data)
        return _relatie_storage[relatie_id].copy()
    except (VTBronnenRelatieNotFound, VTBronnenRelatieInvalidData):
        raise
    except Exception:
        raise VTBronnenRelatieDatabaseError()

def delete_relatie(relatie_id):
    try:
        if relatie_id not in _relatie_storage:
            raise VTBronnenRelatieNotFound()
        del _relatie_storage[relatie_id]
        return None
    except VTBronnenRelatieNotFound:
        raise
    except Exception:
        raise VTBronnenRelatieDatabaseError()

def get_all_relaties():
    try:
        return [item.copy() for item in _relatie_storage.values()]
    except Exception:
        raise VTBronnenRelatieDatabaseError()
