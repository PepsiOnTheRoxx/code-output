from src.api.vtarchivarisrelatieapi_exceptions import (
    RelatieNietGevonden,
    OngeldigeInput,
)

_vtarchivarisrelaties = {}
_next_id = 1

def get_vtarchivarisrelatie(relatie_id):
    relatie = _vtarchivarisrelaties.get(relatie_id)
    if not relatie:
        raise RelatieNietGevonden()
    return relatie.copy()

def create_vtarchivarisrelatie(data):
    global _next_id
    naam = data.get("naam")
    if not naam:
        raise OngeldigeInput()
    relatie = {"id": _next_id, "naam": naam}
    _vtarchivarisrelaties[_next_id] = relatie
    _next_id += 1
    return relatie.copy()

def update_vtarchivarisrelatie(relatie_id, data):
    if relatie_id not in _vtarchivarisrelaties:
        raise RelatieNietGevonden()
    naam = data.get("naam")
    if not naam:
        raise OngeldigeInput()
    _vtarchivarisrelaties[relatie_id]["naam"] = naam
    return _vtarchivarisrelaties[relatie_id].copy()

def delete_vtarchivarisrelatie(relatie_id):
    if relatie_id not in _vtarchivarisrelaties:
        raise RelatieNietGevonden()
    del _vtarchivarisrelaties[relatie_id]
    return None