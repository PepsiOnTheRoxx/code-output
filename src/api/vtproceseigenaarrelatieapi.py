from src.api.vtproceseigenaarrelatieapi_exceptions import (
    RelatieNotFoundException,
    RelatieAlreadyExistsException,
    InvalidRelatieDataException,
)

_relaties = []
_next_id = 1

def get_relatie(relatie_id):
    for relatie in _relaties:
        if relatie["id"] == relatie_id:
            return relatie
    raise RelatieNotFoundException

def create_relatie(relatie_data):
    global _next_id
    if ("proceseigenaar_id" not in relatie_data or
        "facttype_id" not in relatie_data or
        relatie_data.get("proceseigenaar_id") is None or
        relatie_data.get("facttype_id") is None):
        raise InvalidRelatieDataException
    for relatie in _relaties:
        if (relatie["proceseigenaar_id"] == relatie_data["proceseigenaar_id"] and
            relatie["facttype_id"] == relatie_data["facttype_id"]):
            raise RelatieAlreadyExistsException
    new_relatie = {
        "id": _next_id,
        "proceseigenaar_id": relatie_data["proceseigenaar_id"],
        "facttype_id": relatie_data["facttype_id"],
    }
    _relaties.append(new_relatie)
    _next_id += 1
    return new_relatie

def update_relatie(relatie_id, update_data):
    relatie = None
    for r in _relaties:
        if r["id"] == relatie_id:
            relatie = r
            break
    if not relatie:
        raise RelatieNotFoundException
    if "proceseigenaar_id" in update_data and update_data["proceseigenaar_id"] is None:
        raise InvalidRelatieDataException
    if "facttype_id" in update_data and update_data["facttype_id"] is None:
        raise InvalidRelatieDataException
    relatie.update(update_data)
    return relatie

def delete_relatie(relatie_id):
    for i, relatie in enumerate(_relaties):
        if relatie["id"] == relatie_id:
            del _relaties[i]
            return
    raise RelatieNotFoundException

def list_relaties():
    return list(_relaties)