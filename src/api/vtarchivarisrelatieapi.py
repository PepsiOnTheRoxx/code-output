from src.api.vtarchivarisrelatieapi_exceptions import (
    VTArchivarisRelatieAPINotFound,
    VTArchivarisRelatieAPIInvalidInput,
)

_vtarchivarisrelaties = {}
_next_id = 1

def get_vtarchivarisrelatie(relatie_id):
    relatie = _vtarchivarisrelaties.get(relatie_id)
    if not relatie:
        raise VTArchivarisRelatieAPINotFound()
    return relatie.copy()

def create_vtarchivarisrelatie(data):
    global _next_id
    naam = data.get("naam")
    if not naam:
        raise VTArchivarisRelatieAPIInvalidInput()
    relatie = {"id": _next_id, "naam": naam}
    _vtarchivarisrelaties[_next_id] = relatie
    _next_id += 1
    return relatie.copy()

def update_vtarchivarisrelatie(relatie_id, data):
    if relatie_id not in _vtarchivarisrelaties:
        raise VTArchivarisRelatieAPINotFound()
    naam = data.get("naam")
    if not naam:
        raise VTArchivarisRelatieAPIInvalidInput()
    _vtarchivarisrelaties[relatie_id]["naam"] = naam
    return _vtarchivarisrelaties[relatie_id].copy()

def delete_vtarchivarisrelatie(relatie_id):
    if relatie_id not in _vtarchivarisrelaties:
        raise VTArchivarisRelatieAPINotFound()
    del _vtarchivarisrelaties[relatie_id]
    return None
