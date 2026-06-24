from src.api.bronserviceapi_exceptions import BronAPINotFoundException, BronAPIValidationException

_bronnen_db = []
_bron_id_counter = 1


def get_bron_by_id(bron_id):
    for bron in _bronnen_db:
        if bron["id"] == bron_id:
            return bron
    raise BronAPINotFoundException(f"Bron not found")


def create_bron(data):
    global _bron_id_counter
    if not data or "naam" not in data or not data["naam"]:
        raise BronAPIValidationException("Naam mag niet leeg zijn")
    bron = {
        "id": _bron_id_counter,
        "naam": data["naam"]
    }
    _bronnen_db.append(bron)
    _bron_id_counter += 1
    return bron


def update_bron(bron_id, data):
    for bron in _bronnen_db:
        if bron["id"] == bron_id:
            if not data or "naam" not in data or not data["naam"]:
                raise BronAPIValidationException("Naam mag niet leeg zijn")
            bron["naam"] = data["naam"]
            return bron
    raise BronAPINotFoundException("Bron niet gevonden")


def delete_bron(bron_id):
    for idx, bron in enumerate(_bronnen_db):
        if bron["id"] == bron_id:
            del _bronnen_db[idx]
            return True
    raise BronAPINotFoundException("Bron niet gevonden")


def list_bronnen():
    return list(_bronnen_db)
